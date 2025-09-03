import json
from dataclasses import dataclass
from typing import Dict, List

from src.model.interfaces.chat_model_interface import ChatModel


@dataclass
class StageOneResult:
    intent_confirmation: str  # Yes or No response
    response: str
    user_requirements: Dict


class IntentClarityAndConfirmation:
    def __init__(
        self,
        chat_model: ChatModel,
        classify_values_system_message: str,
        intent_confirmation_system_message: str,
        extract_dict_system_message: str,
        function_tool: Dict,
        function_tool_choice: Dict,
    ):
        self.__chat_model = chat_model
        self.__classify_values_system_message = classify_values_system_message
        self.__intent_confirmation_system_message = intent_confirmation_system_message
        self.__extract_dict_system_message = extract_dict_system_message
        self.__function_tool = function_tool
        self.__function_tool_choice = function_tool_choice
        self.__initial_requirements = {
            "price": "-",
            "energy efficiency": "-",
            "cooling capacity": "-",
            "comfort": "-",
            "ac type": "-",
            "smart features": "-",
            "portability": "-",
        }
        self.__user_requirements_dictionary = self.__initial_requirements.copy()

    def run(self) -> StageOneResult:
        """
        This method runs the intent clarification and confirmation layer and results the user requirements dictionary.

        1. Invoking the function calling API all to extract requirements from users input
        2. Handling the tools response by extracting and adding the tool messages to model's conversation history
        3. Adding extracted user requirements dictionary in the conversation
        4. Convert the user requirements i.e. 1.5 tons, fixed unit etc. to its respective values such as essential, standard, or premium
        5. Intent confirmation layer, outputs "Yes" if all requirements are collected otherwise "No" and clarification continues
        6. If intent is confirmed extacts the final user requirements dictionary from the string.
        7. Returns the stage one result for both intent confirmation "Yes" and for "No"
        
        :param StageOneResult: Returns the stage one result with the user requirements dictionary upon intent confirmation.
        """
        # 1). Invoking the function calling API all to extract requirements from users input
        tool_response = self.__chat_model.get_session_response(
            tools=self.__function_tool, tool_choice=self.__function_tool_choice
        )
        
        # 2). Handling the tools response by extracting and adding the tool messages to model's conversation history
        self.__handle_tool_response(tool_response)

        # 3). Adding extracted user requirements dictionary in the conversation
        self.__chat_model.add_message(
            role="assistant",
            content=self.__classify_values_system_message.format(
                json.dumps(self.__user_requirements_dictionary)
            ),
        )

        # 4). Convert the user requirements i.e. 1.5 tons, fixed unit etc. to its respective values such as essential, standard, or premium
        response = self.__chat_model.get_session_response()

        # 5). Intent confirmation layer, outputs "Yes" if all requirements are collected otherwise "No" and clarification continues
        intent_confirmation = self.__intent_confirmation(response[0])

        # 6). If intent is confirmed extacts the final user requirements dictionary from the string.
        user_requirement_dict = {}
        if intent_confirmation[0].lower() == "yes":
            user_requirement_dict = self.__extract_dict_from_string(response[0])
            self.__user_requirements_dictionary = self.__initial_requirements.copy()

        # 7). Returns the stage one result for both intent confirmation "Yes" and for "No"
        return StageOneResult(
            intent_confirmation=intent_confirmation[0],
            response=response[0],
            user_requirements=user_requirement_dict,
        )

    def __intent_confirmation(self, model_response: str) -> List[str]:
        """
        One time OpenAI API call to get intent confirmation with the following steps.
        1. System prompt message and user mesasge is added to messages
        2. One time API call to get the model ersponse

        :param str model_response: Response for the API call with function tools to extract features from user input
        :return List[str]: Returns a single choice response with "Yes" or "No" based on collected features so far
        """
        # 1). System prompt message is added to messages
        messages = [
            {
                "role": "system",
                "content": self.__intent_confirmation_system_message,
            },
            {"role": "user", "content": f"Here is the input: {model_response}"},
        ]

        # 2). One time API call to get the model ersponse
        completion_response = self.__chat_model.preview_response(messages=messages)

        return completion_response

    def __extract_dict_from_string(self, response: str):
        """
        Extracts the features dictionary from string upon intent confirmation

        1. System prompt message and user mesasge is added to messages
        2. Returns one time API call to get the features dictionary
        """
        # 1). System prompt message and user mesasge is added to messages
        messages = [
            {"role": "system", "content": self.__extract_dict_system_message},
            {"role": "user", "content": f"Here is the input: {response}"},
        ]

        # 2). Returns one time API call to get the features dictionary
        response_dict = self.__chat_model.preview_response(messages=messages, json_format=True)
        
        return response_dict

    def __handle_tool_response(self, tool_response):
        """
        This method handles the function tool response to extract features and add it to conversation history.

        1. Access tool_calls, directly with tool_response[0].tool_calls[0] here, but can be accessed like a dictionary too
        2. Access function, directly with tool_call.function here, but can be accessed like a dictionary too
        3. Access arguments, directly with .function.arguments here, but can be access as dictionary too
        4. Store all the values to local dictionary after parsing
        5. Appending tools message from last api call before appending the tool response itself, otherwise LLM wouldn't understand the tool execution

        :param str model_response: Response for the API call with function tools to extract features from user input
        """
        # 1). Access tool_calls, directly with tool_response[0].tool_calls[0] here, but can be accessed like a dictionary too
        tool_call = (
            tool_response[0]["tool_calls"][0]
            if isinstance(tool_response[0], dict)
            else tool_response[0].tool_calls[0]
        )
        # 2). Access function, It can be accessed directly with tool_call.function here, but can be accessed like a Dict too
        func = (
            tool_call["function"] if isinstance(tool_call, dict) else tool_call.function
        )
        # 3). Access arguments, It can be accessed directly with .function.arguments here, but can be access as Dict too
        arguments_json = func["arguments"] if isinstance(func, dict) else func.arguments
        # Parse only if it's a string
        if isinstance(arguments_json, str):
            arguments_json = json.loads(arguments_json)

        # 4). Store all the values to local dictionary after parsing
        for key, value in arguments_json.items():
            self.__user_requirements_dictionary[key] = value

        # 5). Appending tools message from last api call before appending the tool response itself, otherwise LLM wouldn't understand the tool execution
        self.__chat_model.add_message(
            role="assistant", tool_calls=tool_response[0]["tool_calls"]
        )
        self.__chat_model.add_message(
            role="tool",
            tool_call_id=tool_response[0]["id"],
            content=json.dumps(tool_response[0]["content"]),
        )

    def add_message(self, role, content):
        """
        To add a message in messages history.

        :param str role: The roles of the message such as system, user, or assistant
        :param str content: The system message or user message to be sent
        """
        self.__chat_model.add_message(role=role, content=content)

    def clear_messages(self):
        """
        To clear the messages history of this particular stage since the chat can go on forever with the user.
        """
        self.__chat_model.clear_messages()
