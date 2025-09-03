from dataclasses import dataclass
from typing import List

from src.model.interfaces.chat_model_interface import ChatModel


@dataclass
class StageZeroResult:
    response: List[str]


class IntializeConversation:
    def __init__(self, chat_model: ChatModel, system_message: str):
        self.__chat_model = chat_model
        self.system_message = system_message

    def run(self) -> StageZeroResult:
        """
        This method generates the first welcome message to the user by using an LLM API call and initiates the conversation.

        :return StageZeroResult: Returns the LLM's response with the welcome message.
        """
        response = self.__chat_model.get_session_response()

        return StageZeroResult(response=response)

    def add_message(self, role, content):
        """
        To add a message in messages history.

        :param str role: The roles of the message such as system, user, or assistant
        :param str content: The system message or user message to be sent
        :param name
        """
        self.__chat_model.add_message(role=role, content=content)

    def clear_messages(self):
        """
        To clear the messages history of this particular stage since the chat can go on forever with the user.
        """
        self.__chat_model.clear_messages()
