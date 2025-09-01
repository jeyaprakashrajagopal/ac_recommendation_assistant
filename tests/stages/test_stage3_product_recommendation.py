from unittest.mock import call, create_autospec

from src.model.interfaces.chat_model_interface import ChatModel
from src.stages.stage3_product_recommendation import (ProductRecommendations,
                                                      StageThreeResult)


def test_stage_3_calls_intent_confirmation_with_expected_messages():
    chat_model = create_autospec(ChatModel, instance=True)
    system_message = "Display recommendatation and chat with user."
    FAKE_RESPONSE = "lloyd model response"
    fake_response = StageThreeResult(FAKE_RESPONSE)

    chat_model.get_session_response.return_value = FAKE_RESPONSE
    stage_3 = ProductRecommendations(
        chat_model=chat_model, system_message=system_message
    )

    actual = stage_3.run()
    assert actual == fake_response
