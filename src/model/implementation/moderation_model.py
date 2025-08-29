from openai import OpenAI

from src.model.interfaces.moderation_interface import Moderation


class ModerationModel(Moderation):
    def __init__(self):
        self.__client = OpenAI()

    def get_response(self, input_message) -> bool:
        response = self.__client.moderations.create(input=input_message)
        return response.results[0].flagged
