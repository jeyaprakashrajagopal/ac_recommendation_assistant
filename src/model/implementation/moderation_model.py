from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from src.model.interfaces.moderation_interface import Moderation


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
class ModerationModel(Moderation):
    def __init__(self):
        self.__client = OpenAI()

    def get_response(self, input_message) -> bool:
        response = self.__client.moderations.create(input=input_message)
        return response.results[0].flagged
