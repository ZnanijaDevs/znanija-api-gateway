import json


def expect_result(res, file_name: str):
    with open(file_name, encoding="utf-8") as f:
        assert res.json() == json.loads(f.read())
