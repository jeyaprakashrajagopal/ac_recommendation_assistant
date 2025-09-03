from dependency_injector import containers, providers

from src.application import Application
from src.di.model_container import ModelContainer
from src.di.stages_container import StagesContainer
from src.model.implementation.openai_config import OpenAIConfig
from src.pipeline.pipeline import Pipeline


class Container(containers.DeclarativeContainer):
    """
    Main DI container that is responsible for connecting both model and stages here.

    Application class gets created created and the pipeline is injected to access it in the main file.
    """

    config = providers.Configuration()

    openai_config = providers.Singleton(OpenAIConfig)

    model_container = ModelContainer(config=config)
    stages_container = StagesContainer(
        moderation_model=model_container.moderation_model,
        shared_chat_model=model_container.shared_chat_model,
        stage2_chat_model=model_container.stage2_chat_model,
        stage3_chat_model=model_container.stage3_chat_model,
    )
    pipeline = providers.Factory(
        Pipeline,
        moderation_client=model_container.moderation_model,
        stage0=stages_container.stage0,
        stage1=stages_container.stage1,
        stage2=stages_container.stage2,
        stage3=stages_container.stage3,
    )

    application = providers.Factory(Application, pipeline)
