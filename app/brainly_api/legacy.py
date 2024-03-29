from typing import Any

from .exceptions import BrainlyAPIRequestGeneralException, QuestionDoesNotExistException
from .api import Api


class LegacyApiSuccessResponse:
    protocol_version: str
    data: Any
    users_data: list[dict]

    def __init__(self, response: dict):
        self.protocol_version = response["protocol"]
        self.data = response["data"]
        self.users_data = response.get("users_data") or []


class LegacyApi(Api):
    """
    Class that represents the legacy API of Brainly.com (https://brainly.com/api/28).
    Note that this API Will be replaced with the GraphQL one in the future.
    """
    async def _request(
        self,
        api_method: str,
        http_method: str | None = "GET",
        data: Any | None = None
    ) -> LegacyApiSuccessResponse:
        """Make a request to the API (private)"""
        r = await self._make_request(
            url=f"{self.legacy_api_url}/{api_method}",
            method=http_method,
            body=data
        )

        if r["success"] is False:
            raise BrainlyAPIRequestGeneralException(r, source="legacy_api")

        return LegacyApiSuccessResponse(r)

    async def get_users(self, ids: list[int]):
        """Get users by ID"""
        request_path = "api_users/get_by_id"
        for user_id in ids:
            request_path += f"{'?' if request_path.endswith('id') else '&'}id[]={user_id}"

        return await self._request(request_path)

    async def get_question(self, question_id: int):
        """Get question by ID"""
        try:
            question = await self._request(f"api_tasks/main_view/{question_id}")

            if question.data["task"]["user_id"] == 0:
                raise QuestionDoesNotExistException(question_id)

            return question
        except BrainlyAPIRequestGeneralException as exc:
            if exc.exception_type_eq(40):
                raise QuestionDoesNotExistException(question_id)

            raise

    async def get_question_log(self, question_id: int):
        """Get question log by question ID"""
        try:
            return await self._request(f"api_task_lines/big/{question_id}")
        except BrainlyAPIRequestGeneralException as exc:
            if exc.exception_type_eq(170):
                raise QuestionDoesNotExistException(question_id)

            raise

    async def send_message(self, user_id: int, text: str):
        """Send a message to a user"""
        conversation = await self._request("api_messages/check", "post", {
            "user_id": user_id
        })

        conversation_id = conversation.data["conversation_id"]

        return await self._request("api_messages/send", "post", {
            "content": text,
            "conversation_id": conversation_id
        })


legacy_api = LegacyApi()
