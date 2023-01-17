from http import HTTPStatus


def test_get_moderators_list_with_invalid_team(test_app):
    response = test_app.get("/moderators?team=lalal")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_moderators_list(test_app):
    response = test_app.get("/moderators?team=spamouts")
    moderators: list[dict] = response.json()

    assert len(moderators) > 0
