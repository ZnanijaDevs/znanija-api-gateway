from typing import Any

from .exceptions import BrainlyAPIRequestGeneralException, QuestionDoesNotExistException
from .api import Api


class LegacyApi(Api):
    """
    Class that represents Brainly legacy API.
    Will be replaced with Brainly GraphQL API in the future.
    """
    async def _request(
        self,
        api_method: str,
        http_method: str | None = 'get',
        data: Any | None = None
    ) -> dict:
        """Make a request to Brainly legacy API (private)"""
        r = await self._make_request(
            url=f"{self.legacy_api_url}/{api_method}",
            method=http_method,
            body=data
        )

        if r['success'] is False:
            raise BrainlyAPIRequestGeneralException(r, source='legacy_api')

        return r

    async def get_users(self, ids: list[int]) -> list[dict]:
        """Get users by ID"""
        request_path = 'api_users/get_by_id'
        for id in ids:
            request_path += f"{'?' if request_path.endswith('id') else '&'}id[]={id}"

        return await self._request(request_path)

    async def get_question(self, question_id: int):
        """Get question by ID"""
        try:
            question = await self._request(f"api_tasks/main_view/{question_id}")

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
        """Send a message to Brainly user"""
        conversation = await self._request('api_messages/check', 'post', {
            'user_id': user_id
        })

        conversation_id = conversation['data']['conversation_id']

        return await self._request('api_messages/send', 'post', {
            'content': text,
            'conversation_id': conversation_id
        })

legacy_api = LegacyApi()
