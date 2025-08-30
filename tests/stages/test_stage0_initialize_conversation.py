from unittest.mock import call, create_autospec

from src.model.interfaces.chat_model_interface import ChatModel
from src.stages.stage0_initialize_conversation import (
    IntializeConversation,
    StageZeroResult,
)


def test_stage_0_calls_initialize_conversation_with_expected_messages():
    chat_model = create_autospec(ChatModel, instance=True)
    system_message = """
    Act as a smart Air Conditioner recommendation assistant specializing in suggesting right air conditioners to the users based on their requirements. Please strictly stick to the AC assistant context and reply insufficient knowledge in case of any other context.
    """
    FAKE_RESPONSE = "Welcome! I am a bot assistant to help you on selecting an ac!"
    response = StageZeroResult(FAKE_RESPONSE)
    chat_model.get_session_response.return_value = FAKE_RESPONSE

    stage_0 = IntializeConversation(
        chat_model=chat_model, system_message=system_message
    )

    actual = stage_0.run()

    assert actual == response
