from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from src.shared.logger import Logger

from . import validators

logger = Logger(__name__).get_logger()
User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for creating user account"""

    email = serializers.EmailField(
        required=True, validators=[validators.validate_email]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validators.validate_password],
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "age",
            "email",
            "password",
            "confirm_password",
        ]

    def validate(self, data):
        """Validates user data"""

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"Passwords do not match."})
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            logger.error(f"Password validation error: {e}")
            raise serializers.ValidationError(list(e.messages))

        return data

    def create(self, validated_data):
        """Creates user account"""

        validated_data.pop("confirm_password")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])

        return user


class LogInSerializer(serializers.Serializer):
    """Serializer for logging in user"""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, min_length=8
    )

    def validate(self, data):
        """Validate Login details"""

        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if user is None:
                logger.error(f"Invalid email or password for {email}")
                raise serializers.ValidationError("Invalid email or password")

        else:
            logger.error("Both 'email' and 'password' are required")
            raise serializers.ValidationError(
                'Both "email" and "password" are required'
            )

        data["user"] = user
        return data

    def to_representation(self, instance):
        """Response format for login"""

        refresh = RefreshToken.for_user(instance)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"id": instance.id, "email": instance.email},
        }
