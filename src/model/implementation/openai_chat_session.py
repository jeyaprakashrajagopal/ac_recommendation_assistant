import json
from typing import Dict, List, final

from openai import OpenAI

from src.model.interfaces.chat_session_interface import ChatSession


@final
class OpenAIChatSession(ChatSession):
    def __init__(
        self,
        model: str,
        max_tokens: int,
        temperature: float,
        no_of_choices: int,
        seed: int,
    ):
        self.__client = OpenAI()
        self.__messages = []
        self.__model = model
        self.__temperature = temperature
        self.__no_of_choices = no_of_choices
        self.__max_tokens = max_tokens
        self.__seed = seed

    def get_response(self, json_format=False, json_schema=None) -> List[str]:
        if len(self.__messages) == 0:
            raise Exception("Please add a message to start with the conversation!")

        params = {
            "model": self.__model,
            "n": self.__no_of_choices,
            "max_tokens": self.__max_tokens,
            "temperature": self.__temperature,
            "messages": self.__messages,
            "seed": self.__seed,
        }
        if json_format:
            params["response_format"] = {"type": "json_object"}
        elif json_schema is not None:
            params["response_format"] = json_schema

        response = self.__client.chat.completions.create(**params)

        if json_format == True:
            return json.loads(response.choices[0].message.content)
        else:
            return [choice.message.content for choice in response.choices]

    def add_message(self, role: str, content: str, name: str = None) -> None:
        message = {"role": role, "content": content}
        if name != "":
            message["name"] = name
            message["role"] = "system"

        self.__messages.append(message)

    def update_parameters(
        self,
        max_tokens: int = 100,
        model: str = "gpt-3.5-turbo",
        no_of_choices: int = 1,
        temperature: float = 0,
        seed: int = None,
    ) -> None:
        self.__max_tokens = max_tokens
        self.__model = model
        self.__no_of_choices = no_of_choices
        self.__temperature = temperature
        self.__seed = seed

    def get_messages(self) -> List[Dict]:
        return self.__messages

    def reset_messages(self):
        self.__messages = []

    def get_parameters(self) -> List[str]:
        return (
            self.__model,
            self.__max_tokens,
            self.__no_of_choices,
            self.__temperature,
        )
