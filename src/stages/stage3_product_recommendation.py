from dataclasses import dataclass

from src.model.interfaces.chat_model_interface import ChatModel


@dataclass
class StageThreeResult:
    response: str


class ProductRecommendations:
    def __init__(self, chat_model: ChatModel, system_message: str):
        self.__chat_model = chat_model
        self.system_message = system_message

    def run(self) -> StageThreeResult:
        recommendation = self.__chat_model.get_session_response()
        return StageThreeResult(response=recommendation)

    def continue_run(self) -> StageThreeResult:
        response = self.__chat_model.get_session_response()

        return StageThreeResult(response=response)

    def add_message(self, role, content):
        self.__chat_model.add_message(role, content)

    def clear_messages(self):
        self.__chat_model.clear_messages()
