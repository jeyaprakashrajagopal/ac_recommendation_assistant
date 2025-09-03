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
        self.__stage0.add_message(role="system", content=self.__stage0.system_message)

        response = self.__stage0.run()
        return response

    def run_stage1(self, user_input: str) -> StageOneResult:
        self.__moderation_check(user_input)

        self.__stage1.add_message("user", user_input)
        stage1_response = self.__stage1.run()
        self.__moderation_check(stage1_response.response)

        if stage1_response.intent_confirmation.strip() == "No":
            self.__stage1.add_message("assistant", stage1_response.response)

        return stage1_response

    def run_stage2(self, user_requirement: dict) -> StageTwoResult:
        response = self.__stage2.run(user_requirement=user_requirement)
        self.__moderation_check(response.recommendations)

        return response

    def run_stage3(self, recommendations) -> StageThreeResult:
        conversation_recommendation = self.__stage3.system_message.format(
            recommendations
        )
        self.__stage3.add_message("system", conversation_recommendation)

        recommendation = self.__stage3.run()
        self.__moderation_check(recommendation.response)

        self.__stage3.add_message("user", "This is my user profile" + recommendations)
        self.__stage3.add_message("assistant", "\n".join(recommendation.response))
        return recommendation

    def continue_stage3(self, user_input: str) -> StageThreeResult:
        self.__stage3.add_message("user", user_input)
        self.__moderation_check(user_input)
        response = self.__stage3.continue_run()
        self.__stage3.add_message("assistant", "\n".join(response.response))

        return response

    def __moderation_check(self, data):
        flagged = self.__moderation_client.get_response(data)

        if flagged:
            raise ModerationException(self.__ERROR_MESSAGE)

    def clear_messages(self):
        self.__stage0.clear_messages()
        self.__stage1.clear_messages()
        self.__stage2.clear_messages()
        self.__stage3.clear_messages()
