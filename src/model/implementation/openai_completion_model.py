from typing import Dict, List

from openai import OpenAI

from src.model.interfaces.completion_model_interface import TextCompletionModel


class OpenAICompletionModel(TextCompletionModel):
    def __init__(
        self, model: str, max_tokens: int, temperature: float, no_of_choices: int
    ):
        self.__client = OpenAI()
        self.__model = model
        self.__max_tokens = max_tokens
        self.__temperature = temperature
        self.__no_of_choices = no_of_choices

    def get_completion_response(self, prompt) -> List[str | Dict]:
        response = self.__client.completions.create(
            model=self.__model,
            n=self.__no_of_choices,
            temperature=self.__temperature,
            max_tokens=self.__max_tokens,
            prompt=prompt,
        )

        return [choice.text for choice in response.choices]
