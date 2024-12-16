import pytest

from rest_framework.test import APIClient

from tasks.models import User, Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_task(db):
    def make_task(**kwargs):
        return Task.objects.create(**kwargs)

    return make_task


@pytest.fixture
def authenticated_client(db, api_client, create_user):
    user = create_user(username="TestUser", password="Password123")
    api_client.force_authenticate(user)
    return api_client, user
