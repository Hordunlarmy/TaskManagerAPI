from django.urls import path

from .v1 import views

urlpatterns = [
    path("", views.TaskListCreateView.as_view(), name="task-list"),
    path(
        "<uuid:pk>/",
        views.TaskRetrieveUpdateDestroyView.as_view(),
        name="task-detail",
    ),
]
