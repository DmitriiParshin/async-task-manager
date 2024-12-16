import time

from celery import shared_task
from rest_framework.generics import get_object_or_404

from .models import Task


@shared_task
def perform_sum(task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = "in_progress"
    task.save()

    try:
        numbers = task.input_data.get("numbers", [])
        task.result = {"result": sum(numbers)}
        task.status = "completed"
    except Exception as e:
        task.status = "error"
        task.result = {"error": str(e)}

    task.save()


@shared_task
def perform_countdown(task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = "in_progress"
    task.save()

    try:
        seconds = task.input_data.get("seconds", 0)
        time.sleep(seconds)
        task.result = {"message": "Обратный отсчёт завершён"}
        task.status = "completed"
    except Exception as e:
        task.status = "error"
        task.result = {"error": str(e)}

    task.save()
