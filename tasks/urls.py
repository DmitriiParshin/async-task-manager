from django.urls import path
from .views import RegisterView, TaskListView, TaskCreateView, TaskDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
