from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer, CreateTaskSerializer, UserSerializer
from .tasks import perform_sum, perform_countdown

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("id")


class TaskCreateView(generics.CreateAPIView):
    serializer_class = CreateTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if Task.objects.filter(user=user, status__in=["pending", "in_progress"]).count() >= 5:
            raise ValidationError("Вы не можете создать более 5 активных задач.")

        task = serializer.save(user=user)
        if task.task_type == "sum":
            perform_sum.apply_async((task.id,))
        elif task.task_type == "countdown":
            perform_countdown.apply_async((task.id,))


class TaskDetailView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
