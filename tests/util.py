from pathlib import Path
import json
from functools import cache
from httpx import Response


TESTS_DIR_NAME = "tests"


@cache
def expect_result(response: Response, test_data_file_name: str):
    file_path = f"{TESTS_DIR_NAME}/{test_data_file_name}"

    with open(file_path, encoding="utf-8") as f:
        assert response.json() == json.loads(f.read())
