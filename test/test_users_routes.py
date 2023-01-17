USER_ID = 28447645


def test_get_users(test_app):
    res = test_app.post("/brainly/users", json={"ids": [USER_ID]})

    assert res.json() == [{
        "nick": "Аккаунт удален",
        "is_deleted": True,
        "avatar": None,
        "id": USER_ID
    }]


def test_ban_user(test_app):
    BAN_TYPE = 5

    ban_response = test_app.post(f"/brainly/users/{USER_ID}/ban", json={
        "ban_type": BAN_TYPE
    })

    assert ban_response.json() == {
        "ban_type": BAN_TYPE,
        "user_id": USER_ID,
        "banned": True
    }


def test_cancel_ban(test_app):
    cancel_ban_response = test_app.post(f"/brainly/users/{USER_ID}/cancel_ban")
    assert cancel_ban_response.json() == {"ban_cancelled": True}
