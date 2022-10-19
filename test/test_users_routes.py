def test_get_users(test_app):
    res = test_app.post('/brainly/users', json={
        'ids': [1,2]
    })

    assert res.json() == [{
        "nick": "Balrog",
        "id": 1,
        "is_deleted": False,
        "avatar": "https://ru-static.z-dn.net/files/ddd/616daab8d8bd2dc8d799cd8e56f89d56.jpg"
    }, {
        "nick": "miron",
        "id": 2,
        "is_deleted": False,
        "avatar": None
    }]
