from dependency_injector import providers

from src.model.implementation.moderation_model import ModerationModel
from src.model.implementation.openai_chat_model import OpenAIChatModel


class ModelContainer:
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

        self.chat_model = providers.Singleton(OpenAIChatModel, **common_kwargs)

        self.moderation_model = providers.Factory(ModerationModel)
