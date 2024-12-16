from django.urls import reverse
from rest_framework import status


def test_register_user(db, api_client):
    url = reverse("register")
    payload = {"username": "newuser", "password": "password123"}

    response = api_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["username"] == "newuser"


def test_create_task_sum(db, authenticated_client):
    api_client, user = authenticated_client
    url = reverse("task-create")
    payload = {
        "task_type": "sum",
        "input_data": {"numbers": [1, 2, 3]},
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["task_type"] == "sum"
    assert response.data["input_data"] == {"numbers": [1, 2, 3]}


def test_create_task_countdown(db, authenticated_client):
    api_client, user = authenticated_client
    url = reverse("task-create")
    payload = {
        "task_type": "countdown",
        "input_data": {"seconds": 15},
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["task_type"] == "countdown"
    assert response.data["input_data"] == {"seconds": 15}


def test_create_task_invalid_type(db, authenticated_client):
    api_client, user = authenticated_client
    url = reverse("task-create")
    payload = {
        "task_type": "invalid_type",
        "input_data": {},
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "task_type" in response.data


def test_create_task_exceeds_limit(db, authenticated_client, create_task):
    api_client, user = authenticated_client

    # Создаем 5 активных задач
    for _ in range(5):
        create_task(user=user, task_type="sum", status="pending", input_data={})

    url = reverse("task-create")
    payload = {
        "task_type": "sum",
        "input_data": {"numbers": [1, 2, 3]},
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Вы не можете создать более 5 активных задач." in str(response.data)
