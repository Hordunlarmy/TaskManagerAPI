from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from src.shared.logger import Logger

from .serializers import LogInSerializer, RegisterUserSerializer

logger = Logger(__name__).get_logger()
User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    """Register a new user."""

    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"User {user.email} created successfully.")


class LoginUserView(generics.GenericAPIView):
    """Login User"""

    serializer_class = LogInSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        logger.info(
            f"User {serializer.validated_data['user'].email} logged in."
        )
        user = serializer.validated_data["user"]
        return Response(
            serializer.to_representation(user),
            status=status.HTTP_200_OK,
        )


class LogoutUserView(generics.GenericAPIView):
    """Logout user and blacklist token."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        refresh_token = request.headers.get("X-Refresh-Token")
        access_token = request.headers.get("Authorization")
        if access_token and access_token.startswith("Bearer "):
            access_token = access_token[len("Bearer ") :]  # noqa

        if refresh_token is None:
            return Response(
                {
                    "status": "error",
                    "message": "X-Refresh-Token header not provided.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if refresh_token.startswith("Bearer "):
            refresh_token = refresh_token.split(" ")[1]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"status": "success", "message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
