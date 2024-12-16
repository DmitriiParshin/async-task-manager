from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "task_type", "input_data", "status", "result", "created_at"]
        read_only_fields = ["status", "result", "created_at"]


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["task_type", "input_data"]

    def validate_task_type(self, value):
        if value not in ["sum", "countdown"]:
            raise serializers.ValidationError(f"Задач типа '{value}' не существует.")
        return value

    def validate_input_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Поле `input_data` должно быть объектом JSON.")

        task_type = self.initial_data.get("task_type")
        if task_type == "sum":
            numbers = value.get("numbers")
            if not numbers:
                raise serializers.ValidationError(
                    "Для задач типа 'sum' поле `numbers` должно быть обязательным."
                )
            if not isinstance(numbers, list) or not all(
                isinstance(num, (int, float)) for num in numbers
            ):
                raise serializers.ValidationError(
                    "Для задач типа 'sum' поле `numbers` должно быть списком чисел."
                )

        if task_type == "countdown":
            seconds = value.get("seconds")
            if not seconds:
                raise serializers.ValidationError(
                    "Для задач типа 'countdown' поле `seconds` должно быть обязательным."
                )
            if not isinstance(seconds, int) or seconds < 1:
                raise serializers.ValidationError(
                    "Для задач типа 'countdown' поле `seconds` должно быть положительным целым числом."
                )

        return value
