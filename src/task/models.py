from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from src.shared.basemodel import BaseModel
from src.shared.email import sender


class Task(BaseModel):
    """
    Model representing a task.
    """

    STATUS_CHOICES = (
        ("Incomplete", "Incomplete"),
        ("Complete", "Complete"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Incomplete"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Task)
def send_status_change_email(instance, **kwargs):
    """
    Send an email to the user when the task status is changed to
    'Complete'.
    """
    if instance.pk and instance.status == "Complete":
        try:
            previous_task = Task.objects.get(pk=instance.pk)
            if previous_task.status != "Complete":
                user = instance.user

                sender.send_status_email(
                    recipient_email=user.email,
                    recipient_name=user.first_name,
                    template_variables={
                        "name": user.first_name,
                        "task_name": instance.name,
                        "task_status": instance.status,
                        "task_desc": instance.description,
                        "task_time": instance.created_at,
                    },
                )
        except Task.DoesNotExist:
            if instance.status == "Complete":
                user = instance.user

                sender.send_new_user_verification(
                    recipient_email=user.email,
                    recipient_name=user.first_name,
                    template_variables={
                        "name": user.first_name,
                        "task_name": instance.name,
                        "task_status": instance.status,
                        "task_desc": instance.description,
                        "task_time": instance.created_at,
                    },
                )
