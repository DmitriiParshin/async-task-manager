from tasks.tasks import perform_sum, perform_countdown


def test_perform_sum_success(db, create_user, create_task):
    user = create_user(username="TestUser", password="Password123")
    task = create_task(
        user=user,
        task_type="sum",
        input_data={"numbers": [1, 2, 3]},
        status="pending",
    )
    perform_sum(task.id)

    task.refresh_from_db()
    assert task.status == "completed"
    assert task.result == {"result": 6}


def test_perform_sum_invalid_data(db, create_user, create_task):
    user = create_user(username="TestUser", password="Password123")
    task = create_task(
        user=user,
        task_type="sum",
        input_data={"numbers": "invalid_data"},
        status="pending",
    )
    perform_sum(task.id)

    task.refresh_from_db()
    assert task.status == "error"
    assert "error" in task.result


def test_perform_countdown_success(db, create_user, create_task):
    user = create_user(username="TestUser", password="Password123")
    task = create_task(
        user=user,
        task_type="countdown",
        input_data={"seconds": 1},
        status="pending",
    )
    perform_countdown(task.id)

    task.refresh_from_db()
    assert task.status == "completed"
    assert task.result == {"message": "Обратный отсчёт завершён"}


def test_perform_countdown_invalid_data(db, create_user, create_task):
    user = create_user(username="TestUser", password="Password123")
    task = create_task(
        user=user,
        task_type="countdown",
        input_data={"seconds": "invalid_data"},
        status="pending",
    )
    perform_countdown(task.id)

    task.refresh_from_db()
    assert task.status == "error"
    assert "error" in task.result
