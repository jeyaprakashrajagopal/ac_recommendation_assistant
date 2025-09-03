from dependency_injector import providers

from src.model.implementation.moderation_model import ModerationModel
from src.model.implementation.openai_chat_model import OpenAIChatModel


class ModelContainer:
    """ Invoking Factory to create instances of the ChatModel, Moderation classes """
    def __init__(self, config):
        __DEFAULT_MODEL = "gpt-4o-mini"
        __MAX_TOKENS = 500
        __TEMPERATURE = 0
        __NO_OF_CHOICES = 1
        __SEED = 7248

        common_kwargs = {
            "model": config.model() or __DEFAULT_MODEL,
            "max_tokens": config.max_tokens() or __MAX_TOKENS,
            "temperature": config.temperature() or __TEMPERATURE,
            "no_of_choices": config.no_of_choices() or __NO_OF_CHOICES,
            "seed": config.no_of_choices() or __SEED,
        }

        # Shared chat model is used on both stage 0 (initialize conversation) and stage 1
        self.shared_chat_model = providers.Singleton(OpenAIChatModel, **common_kwargs)
        # Independent chat model is used on both stage 2 and stage 3
        self.stage2_chat_model = providers.Factory(OpenAIChatModel, **common_kwargs)
        self.stage3_chat_model = providers.Factory(OpenAIChatModel, **common_kwargs)
        self.moderation_model = providers.Factory(ModerationModel)
