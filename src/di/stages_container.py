from dependency_injector import providers

from config.settings import *
from src.pipeline.pipeline import Pipeline
from src.stages.stage0_initialize_conversation import IntializeConversation
from src.stages.stage1_intent_confirmation import IntentClarityAndConfirmation
from src.stages.stage2_product_extraction import ProductExtractionAndMapping
from src.stages.stage3_product_recommendation import ProductRecommendations
from src.utils.templating import (load_dictionary_from_md,
                                  load_system_message_without_params)


class StagesContainer:
    """Invoking Factory to create instances of the stages, separate instances created and chat models are injected here"""

    def __init__(
        self, moderation_model, shared_chat_model, stage2_chat_model, stage3_chat_model
    ):
        stage0_system_message = load_system_message_without_params(
            STAGE0_SYSTEM_MESSAGE
        )
        self.stage0 = providers.Factory(
            IntializeConversation,
            chat_model=shared_chat_model,
            system_message=stage0_system_message,
        )

        stage1_system_message = load_system_message_without_params(
            STAGE1_SYSTEM_MESSAGE
        )
        stage1_classify_values_system_message = load_system_message_without_params(
            STAGE1_CLASSIFY_VALUES_SYSTEM_MESSAGE
        )
        extract_dict_system_message = load_system_message_without_params(
            EXTRACT_DICT_SYS_MSG
        )
        stage1_function_tool = load_dictionary_from_md(STAGE1_FUNCTION_TOOL)
        stage1_function_tool_choice = load_dictionary_from_md(
            STAGE1_FUNCTION_TOOL_CHOICE
        )

        self.stage1 = providers.Factory(
            IntentClarityAndConfirmation,
            chat_model=shared_chat_model,
            classify_values_system_message=stage1_classify_values_system_message,
            intent_confirmation_system_message=stage1_system_message,
            extract_dict_system_message=extract_dict_system_message,
            function_tool=stage1_function_tool,
            function_tool_choice=stage1_function_tool_choice,
        )

        stage2_system_message = load_system_message_without_params(
            STAGE2_SYSTEM_MESSAGE
        )
        self.stage2 = providers.Factory(
            ProductExtractionAndMapping,
            chat_model=stage2_chat_model,
            system_message=stage2_system_message,
        )

        stage3_system_message = load_system_message_without_params(
            STAGE3_SYSTEM_MESSAGE
        )
        self.stage3 = providers.Factory(
            ProductRecommendations,
            chat_model=stage3_chat_model,
            system_message=stage3_system_message,
        )

        self.pipeline = providers.Factory(
            Pipeline,
            moderation_model,
            self.stage0,
            self.stage1,
            self.stage2,
            self.stage3,
        )
