from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Запланировано"),
        ("in_progress", "Выполняется"),
        ("completed", "Выполнено"),
        ("error", "Ошибка"),
    ]

    TASK_TYPE_CHOICES = [
        ("sum", "Суммирование"),
        ("countdown", "Обратный отсчёт"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    input_data = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
