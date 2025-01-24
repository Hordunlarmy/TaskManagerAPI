from rest_framework import serializers

from src.task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    """

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "status",
            "created_at",
        ]

    def validate_status(self, value):
        """
        Custom validation to ensure status is either
        'Incomplete' or 'Complete'.
        """
        if value not in dict(Task.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid status value.")
        return value

    def update(self, instance, validated_data):
        """
        Override the update method to handle status changes and other fields.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
