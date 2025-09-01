import json
from typing import Dict, List, final

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from src.model.interfaces.chat_model_interface import ChatModel


@final
class OpenAIChatModel(ChatModel):
    def __init__(
        self,
        model: str,
        max_tokens: int,
        temperature: float,
        no_of_choices: int,
        seed: int,
    ):
        self.__client = OpenAI()
        self.__model = model
        self.__temperature = temperature
        self.__no_of_choices = no_of_choices
        self.__max_tokens = max_tokens
        self.__seed = seed
        self.__messages = []

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def preview_response(
        self, messages: List[Dict], json_format=False, json_schema=None
    ) -> List[str | Dict]:
        if len(messages) == 0:
            raise Exception("Please add a message to start with the conversation!")

        params = {
            "model": self.__model,
            "n": self.__no_of_choices,
            "max_tokens": self.__max_tokens,
            "temperature": self.__temperature,
            "messages": messages,
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

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def get_session_response(
        self, json_format=False, json_schema=None, tools=None, tool_choice: Dict = None
    ) -> List[str]:
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
        elif tools is not None:
            params["tools"] = [tools]
            params["tool_choice"] = tool_choice

        response = self.__client.chat.completions.create(**params)

        if json_format == True:
            return json.loads(response.choices[0].message.content)
        else:
            return self.__return_tools_result(response=response)

    def add_message(
        self,
        role: str,
        content: str = None,
        name: str = None,
        tool_calls: List[Dict] = None,
        tool_call_id: str = None,
    ) -> None:
        message = {"role": role, "content": content}
        if name is not None:
            message["name"] = name
            message["role"] = "system"
        elif tool_call_id is not None:
            message["tool_call_id"] = tool_call_id
        elif tool_calls is not None:
            message["tool_calls"] = tool_calls

        self.__messages.append(message)

    def add_chat_completion_message(self, message) -> None:
        self.__messages.append(message)

    def clear_messages(self):
        self.__messages = []

    def get_messages(self):
        return self.__messages

    def update_parameters(
        self,
        max_tokens: int = 100,
        model: str = "gpt-3.5-turbo",
        no_of_choices: int = 1,
        temperature: float = 0,
        seed=None,
    ) -> None:
        self.__max_tokens = max_tokens
        self.__model = model
        self.__no_of_choices = no_of_choices
        self.__temperature = temperature
        self.__seed = seed

    def __return_tools_result(self, response):
        results = []
        for choice in response.choices:
            if choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    results.append(
                        {
                            "id": tool_call.id,
                            "content": args,
                            "tool_calls": response.choices[0].message.tool_calls,
                        }
                    )
            elif choice.message.content:
                results.append(choice.message.content)

        return results
