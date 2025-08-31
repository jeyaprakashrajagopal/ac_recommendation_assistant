import json
from dataclasses import dataclass
from typing import Dict, List

from src.model.interfaces.chat_model_interface import ChatModel


@dataclass
class StageOneResult:
    intent_confirmation: str  # yes or no
    response: str
    user_requirements: Dict


class IntentClarityAndConfirmation:
    def __init__(
        self,
        chat_model: ChatModel,
        system_message: str,
        extract_dict_system_message: str,
        tools: Dict,
        tools_choice: Dict,
    ):
        self.__chat_model = chat_model
        self.__system_message = system_message
        self.__extract_dict_system_message = extract_dict_system_message
        self.tools = tools
        self.tools_choice = tools_choice
        self.__initial_requirements = {
            "price": "-",
            "energy efficiency": "-",
            "cooling capacity": "-",
            "comfort": "-",
            "ac type": "-",
            "smart features": "-",
            "portability": "-",
        }
        self.__user_requirements_dictionary = self.__initial_requirements

    def run(self) -> StageOneResult:
        # Making use of tools to extract user primary features of the product from user's input
        tool_response = self.__chat_model.get_session_response(
            tools=self.tools, tool_choice=self.tools_choice
        )
        self.__handle_tool_response(tool_response)
        # Making use of tools to extract user primary features of the product from user's input
        response = self.__chat_model.get_session_response()
        intent_confirmation = self.__intent_confirmation(response[0])

        user_requirement_dict = {}
        if intent_confirmation[0].lower() == "yes":
            user_requirement_dict = self.__extract_dict_from_string(response[0])
            self.__user_requirements_dictionary = self.__initial_requirements

        return StageOneResult(
            intent_confirmation=intent_confirmation[0],
            response=response[0],
            user_requirements=user_requirement_dict,
        )

    def __intent_confirmation(self, model_response: str) -> List[str]:
        messages = [
            {
                "role": "system",
                "content": self.__system_message.format(model_response=model_response),
            },
            {"role": "user", "content": f"Here is the input: {model_response}"},
        ]

        completion_response = self.__chat_model.preview_response(messages=messages)
        return completion_response

    def __extract_dict_from_string(self, response: str):
        messages = [
            {"role": "system", "content": self.__extract_dict_system_message},
            {"role": "user", "content": f"Here is the input: {response}"},
        ]

        return self.__chat_model.preview_response(messages=messages, json_format=True)

    def add_message(self, role, content):
        self.__chat_model.add_message(role=role, content=content)

    def clear_messages(self):
        self.__chat_model.clear_messages()

    def __handle_tool_response(self, tool_response):
        tool_call = (
            tool_response[0]["tool_calls"][0]
            if isinstance(tool_response[0], dict)
            else tool_response[0].tool_calls[0]
        )

        # Access function
        func = (
            tool_call["function"] if isinstance(tool_call, dict) else tool_call.function
        )

        # Get arguments JSON
        arguments_json = func["arguments"] if isinstance(func, dict) else func.arguments
        # Parse only if it's a string
        if isinstance(arguments_json, str):
            arguments_json = json.loads(arguments_json)

        for key, value in arguments_json.items():
            self.__user_requirements_dictionary[key] = value

        # Appending tools message from last api call before appending the tool response itself, otherwise it won't be allowed as per openai rules
        self.__chat_model.add_message(
            role="assistant", tool_calls=tool_response[0]["tool_calls"]
        )
        self.__chat_model.add_message(
            role="tool",
            tool_call_id=tool_response[0]["id"],
            content=json.dumps(tool_response[0]["content"]),
        )
        self.__chat_model.add_message(
            role="assistant",
            content=f"Current collected requirements are: {self.__user_requirements_dictionary} and please convert it to values if all features are collected as specified to meet the expectations.",
        )
