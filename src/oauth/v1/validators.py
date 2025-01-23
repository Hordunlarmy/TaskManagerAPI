from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def validate_email(value):
    """Validate provided email"""

    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError(
            "Account already exist. Please login.",
        )
    return value


def validate_password(value):
    """Validates provided password"""

    if len(value) < 8:
        raise serializers.ValidationError(
            "Password must be minimum of eight(8) characters",
        )
    return value
