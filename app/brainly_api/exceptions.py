from typing import Any


class BrainlyAPIRequestGeneralException(Exception):
    error_details: list[Any] | str = ''
    source: str

    def __init__(
        self,
        error_details: list[Any] | str | None = None,
        source: str | None = None
    ):
        self.error_details = error_details
        self.source = source

        super().__init__(f"[{source}] Brainly API exception: {error_details}")

    def exception_type_eq(self, exception_type: int) -> bool:
        """Check whether the exception type equals another one"""
        if not isinstance(self.error_details, dict):
            return False

        return self.error_details['exception_type'] == exception_type


class QuestionDoesNotExistException(Exception):
    question_id: int

    def __init__(self, question_id: int):
        self.question_id = question_id

        super().__init__(f"Question {question_id} does not exist")
