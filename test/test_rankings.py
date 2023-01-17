from http import HTTPStatus


def test_get_daily_moderator_rankings(test_app):
    response = test_app.get("/brainly/ranking/moderators/daily")
    rankings = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(rankings) > 0
