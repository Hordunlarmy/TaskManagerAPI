from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .v1 import views

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="user-register"),
    path("login/", views.LoginUserView.as_view(), name="user-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.LogoutUserView.as_view(), name="user-logout"),
]
