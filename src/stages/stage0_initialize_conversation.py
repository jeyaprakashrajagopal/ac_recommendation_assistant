from dataclasses import dataclass
from typing import Dict

from src.model.interfaces.chat_model_interface import ChatModel


@dataclass
class StageZeroResult:
    response: str


class IntializeConversation:
    def __init__(self, chat_model: ChatModel, system_message: str):
        self.__chat_model = chat_model
        self.system_message = system_message

    def run(self) -> StageZeroResult:
        response = self.__chat_model.get_session_response()
        return StageZeroResult(response=response)

    def add_message(self, role, content, name=None):
        self.__chat_model.add_message(role=role, name=name, content=content)

    def clear_messages(self):
        self.__chat_model.clear_messages()
