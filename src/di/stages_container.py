from dependency_injector import providers

from config.settings import *
from src.pipeline.pipeline import Pipeline
from src.stages.stage0_initialize_conversation import IntializeConversation
from src.stages.stage1_intent_confirmation import IntentClarityAndConfirmation
from src.stages.stage2_product_extraction import ProductExtractionAndMapping
from src.stages.stage3_product_recommendation import ProductRecommendations
from src.utils.templating import (
    load_dictionary_from_md,
    load_system_message_without_params,
)


class StagesContainer:
    def __init__(self, moderation_model, chat_model):
        stage0_system_message = load_system_message_without_params(
            STAGE0_SYSTEM_MESSAGE
        )
        self.stage0 = providers.Factory(
            IntializeConversation,
            chat_model=chat_model,
            system_message=stage0_system_message,
        )

        stage1_system_message = load_system_message_without_params(
            STAGE1_SYSTEM_MESSAGE
        )
        extract_dict_system_message = load_system_message_without_params(
            EXTRACT_DICT_SYS_MSG
        )
        stage1_tools = load_dictionary_from_md(STAGE1_TOOLS)
        stage1_tools_choice = load_dictionary_from_md(STAGE1_TOOLS_CHOICE)

        self.stage1 = providers.Factory(
            IntentClarityAndConfirmation,
            chat_model=chat_model,
            system_message=stage1_system_message,
            extract_dict_system_message=extract_dict_system_message,
            tools=stage1_tools,
            tools_choice=stage1_tools_choice,
        )

        stage2_system_message = load_system_message_without_params(
            STAGE2_SYSTEM_MESSAGE
        )
        self.stage2 = providers.Factory(
            ProductExtractionAndMapping,
            chat_model=chat_model,
            system_message=stage2_system_message,
        )

        stage3_system_message = load_system_message_without_params(
            STAGE3_SYSTEM_MESSAGE
        )
        self.stage3 = providers.Factory(
            ProductRecommendations,
            chat_model=chat_model,
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
