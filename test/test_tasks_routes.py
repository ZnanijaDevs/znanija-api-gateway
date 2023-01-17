from http import HTTPStatus
from . import expect_result


def test_get_task_with_invalid_id(test_app):
    res = test_app.get("/task/-5")
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_task(test_app):
    res = test_app.get("/task/2")
    expect_result(res, "test/responses/get_task.json")


def test_get_task_log(test_app):
    res = test_app.get("/task/log/50444984")
    expect_result(res, "test/responses/get_task_log.json")


def test_check_deleted_tasks(test_app):
    res = test_app.post("/task/deleted_tasks", json={
        "ids": [1, 2, 3]
    })

    expect_result(res, "test/responses/check_deleted_tasks.json")
