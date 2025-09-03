from typing import Dict

from src.model.interfaces.moderation_interface import Moderation
from src.stages.stage0_initialize_conversation import (IntializeConversation,
                                                       StageZeroResult)
from src.stages.stage1_intent_confirmation import (
    IntentClarityAndConfirmation, StageOneResult)
from src.stages.stage2_product_extraction import (ProductExtractionAndMapping,
                                                  StageTwoResult)
from src.stages.stage3_product_recommendation import (ProductRecommendations,
                                                      StageThreeResult)
from src.utils.ModerationException import ModerationException


class Pipeline:
    """
    Orchestrates the workflow of the project by running different stages.

    This pipeline is responsible for the following
    1. Adding user and assistant messages to chat model's message history.
    2. Moderation checks and throws an exception in case of failure
    3. Internal processing happens on individual stages where each stage is responsible for updating the message history i.e.
        * In stage 1, Function calling tool response.
        * In stage 2, One time responses such as extacting features dictionary from description
    4. System messages are kept in individual stages rather than putting all in one place
    """

    def __init__(
        self,
        moderation_client: Moderation,
        stage0: IntializeConversation,
        stage1: IntentClarityAndConfirmation,
        stage2: ProductExtractionAndMapping,
        stage3: ProductRecommendations,
    ):
        self.__moderation_client = moderation_client
        self.__stage0 = stage0
        self.__stage1 = stage1
        self.__stage2 = stage2
        self.__stage3 = stage3
        self.__ERROR_MESSAGE = "This conversation ends now since your input has some sensitive content. Please start the new conversation to continue!"

    def run_stage0(self) -> StageZeroResult:
        """
        Initializes the conversation with the user by invoking stage 0, where a system message is added.

        :return StageZeroResult: Returns stage 0 result.
        """
        # 1). Adds system message to model's message history
        self.__stage0.add_message(role="system", content=self.__stage0.system_message)

        # 2). Runs stage zero
        response = self.__stage0.run()

        return response

    def run_stage1(self, user_input: str) -> StageOneResult:
        """
        Runs stage 1 for intent clarification and confirmation, and outputs user requirements dictionary. The following steps are executed

        1. Moderation check on user input
        2. Adds user input to the message history
        3. Runs stage 1
        4. Executing the moderation check on LLM's output
        5. Add LLM's response to message history if some requirements are still missing

        :param str user_input: User's input message
        :return StageOneResult: Returns stage 1 starts running clarification loop until user requirements dictionary is extracted.
        :raises ModerationException: Throws the custom exception
        """
        # 1). Moderation check on user input
        self.__moderation_check(user_input)

        # 2). Adds user input to message history
        self.__stage1.add_message("user", user_input)

        # 3). Runs stage 1
        stage1_response = self.__stage1.run()

        # 4). Moderation check on LLM's response
        self.__moderation_check(stage1_response.response)

        # 5). If intent clarification is not complete, add the assistant message to the message history
        if stage1_response.intent_confirmation.strip() == "No":
            self.__stage1.add_message("assistant", stage1_response.response)

        return stage1_response

    def run_stage2(self, user_requirement: Dict) -> StageTwoResult:
        """
        Runs stage 2 for intent clarification and confirmation, and outputs user requirements dictionary. The following steps are executed

        :param Dict user_requirement: Collected user requirement's dictionary
        :return StageTwoResult: Returns stage 2 result with the product recommendations.
        :raises ModerationException: Throws the custom exception
        """
        # 1). Runs stage 2
        response = self.__stage2.run(user_requirement=user_requirement)

        # 2). Moderation check on the LLM's response
        self.__moderation_check(response.recommendations)

        return response

    def run_stage3(self, recommendations) -> StageThreeResult:
        """
        Runs stage 3 by showing the recommendations to the user. The following steps are executed

        1. Appending user requirements dictionary to system message, then add it to message history
        2. Start running stage 2 by generating recommendations that can be displayed to the user
        3. Executing the moderation check on LLM's output
        4. Add recommendations and assistant's response in previous step to message history

        :param Dict: User's input message
        :return StageOneResult: Returns stage 1 result with the user requirements dictionary.
        :raises ModerationException: Throws the custom exception
        """
        # 1). Appending user requirements to system message and add it to message history
        conversation_recommendation = self.__stage3.system_message.format(
            recommendations
        )
        self.__stage3.add_message("system", conversation_recommendation)

        # 2). Run stage 3
        recommendation = self.__stage3.run()

        # 3). Moderation check on LLM's response
        self.__moderation_check(recommendation.response)

        # 4). Add recommendations and assistant's response in previous step to message history
        self.__stage3.add_message("user", "This is my user profile" + recommendations)
        self.__stage3.add_message("assistant", "\n".join(recommendation.response))

        return recommendation

    def continue_stage3(self, user_input: str) -> StageThreeResult:
        """
        Continues to run stage 3 by keeping the user engaged with doubt resolution session.

        1. Adds user message to message history of the model
        2. Moderation check on user input
        3. Continues to run stage 3
        4. Moderation check on LLM's response
        5. Add's LLM response to model's message history

        :param Dict: User's input message
        :return StageOneResult: Returns stage 1 result with the user requirements dictionary.
        :raises ModerationException: Throws the custom exception
        """
        # 1). Adds user message to message history
        self.__stage3.add_message("user", user_input)

        # 2). Moderation check on user input
        self.__moderation_check(user_input)

        # 3). Continue running stage 3
        response = self.__stage3.continue_run()

        # 4). Moderation check on LLM' output
        response_str = "\n".join(response.response)
        self.__moderation_check(response_str)

        # 5). Add assistant message to message history
        self.__stage3.add_message("assistant", "\n".join(response_str))

        return StageThreeResult(response.response)

    def __moderation_check(self, data):
        """
        Runs the moderation check and returns the flag

        :param str data: Data on which the moderation check
        :raises ModerationException: Throws the custom exception
        """
        flagged = self.__moderation_client.get_response(data)

        if flagged:
            raise ModerationException(self.__ERROR_MESSAGE)

    def clear_messages(self):
        """
        Clears the chat message history on all stages.
        """
        self.__stage0.clear_messages()
        self.__stage1.clear_messages()
        self.__stage2.clear_messages()
        self.__stage3.clear_messages()
