from django.conf import settings
from django.db import models

from src.shared.basemodel import BaseModel


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

    def get_status_display(self):
        """
        Returns the human-readable status of the task.
        """
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")

    def update_status(self, status):
        """
        Updates the status of the task.
        """
        if status in dict(self.STATUS_CHOICES):
            self.status = status
            self.save()

    def mark_as_complete(self):
        """
        Marks the task as complete.
        """
        self.update_status("Complete")

    def mark_as_incomplete(self):
        """
        Marks the task as incomplete.
        """
        self.update_status("Incomplete")
