import pytest
from rest_framework.exceptions import ValidationError

from tasks.serializers import CreateTaskSerializer


def test_valid_task_sum_serializer():
    data = {
        "task_type": "sum",
        "input_data": {"numbers": [1, 2, 3]},
    }

    serializer = CreateTaskSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["task_type"] == "sum"
    assert serializer.validated_data["input_data"] == {"numbers": [1, 2, 3]}


def test_valid_task_countdown_serializer():
    data = {
        "task_type": "countdown",
        "input_data": {"seconds": 15},
    }

    serializer = CreateTaskSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["task_type"] == "countdown"
    assert serializer.validated_data["input_data"] == {"seconds": 15}


def test_invalid_task_type_serializer():
    data = {
        "task_type": "invalid",
        "input_data": {},
    }

    serializer = CreateTaskSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_invalid_input_data_for_sum():
    data = {
        "task_type": "sum",
        "input_data": {"numbers": "not_a_list"},
    }

    serializer = CreateTaskSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_invalid_input_data_for_countdown():
    data = {
        "task_type": "countdown",
        "input_data": {"seconds": -5},
    }

    serializer = CreateTaskSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
