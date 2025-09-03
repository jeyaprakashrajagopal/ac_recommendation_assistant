from dataclasses import dataclass
from typing import List

from src.model.interfaces.chat_model_interface import ChatModel


@dataclass
class StageThreeResult:
    response: List[str]


class ProductRecommendations:
    def __init__(self, chat_model: ChatModel, system_message: str):
        self.__chat_model = chat_model
        self.system_message = system_message

    def run(self) -> StageThreeResult:
        """
        This method actually runs the final stage of the pipeling

        :return StageThreeResult: Data class that contains the recommendations
        """
        recommendation = self.__chat_model.get_session_response()

        return StageThreeResult(response=recommendation)

    def continue_run(self) -> StageThreeResult:
        """
        This method responds to user query through an LLM API call.

        :return StageThreeResult: Data class that contains the response
        """
        response = self.__chat_model.get_session_response()

        return StageThreeResult(response=response)

    def add_message(self, role, content):
        """
        To add a message in messages history.

        :param str role: The roles of the message such as system, user, or assistant
        :param str content: The system message or user message to be sent
        """
        self.__chat_model.add_message(role, content)

    def clear_messages(self):
        """
        To clear the messages history of this particular stage since the chat can go on forever with the user.
        """
        self.__chat_model.clear_messages()
