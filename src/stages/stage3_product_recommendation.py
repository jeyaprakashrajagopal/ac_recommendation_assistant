from dataclasses import dataclass

from src.model.interfaces.chat_model_interface import ChatModel


@dataclass
class StageThreeResult:
    response: str


class ProductRecommendatations:
    def __init__(self, chat_model: ChatModel, system_message: str):
        self.__chat_model = chat_model
        self.system_message = system_message
        self.messages = []

    def run(self) -> StageThreeResult:
        recommendation = self.__chat_model.preview_response(messages=self.messages)
        return StageThreeResult(response=recommendation)

    def continue_run(self) -> StageThreeResult:
        response = self.__chat_model.preview_response(messages=self.messages)

        return StageThreeResult(response=response)

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def clear_messages(self):
        self.__chat_model.clear_messages()
