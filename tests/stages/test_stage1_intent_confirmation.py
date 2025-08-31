from unittest.mock import MagicMock

import pytest

from src.stages.stage1_intent_confirmation import (
    IntentClarityAndConfirmation, StageOneResult)


@pytest.fixture
def mock_chat_model():
    return MagicMock()


@pytest.fixture
def intent_clarity_and_confirmation(mock_chat_model):
    return IntentClarityAndConfirmation(
        chat_model=mock_chat_model,
        system_message="System: {model_response}",
        extract_dict_system_message="Extract dict system message",
        tools={"tool1": "desc"},
        tools_choice={"tool1": "testing"},
    )


def test_stage1_intent_confirmation_produces_user_requirements(
    intent_clarity_and_confirmation, mock_chat_model
):
    tool_response = [
        {
            "tool_calls": [{"type": "test_tool", "function": {"arguments": {}}}],
            "id": "tool_id_1",
            "content": {"feature": "value"},
        }
    ]

    main_response = [""]
    intent_confirmation = ["Yes"]
    extracted_dict = {"feature": "value"}

    mock_chat_model.get_session_response.side_effect = [tool_response, main_response]
    intent_clarity_and_confirmation._IntentClarityAndConfirmation__intent_confirmation = MagicMock(
        return_value=intent_confirmation
    )
    intent_clarity_and_confirmation._IntentClarityAndConfirmation__extract_dict_from_string = MagicMock(
        return_value=extracted_dict
    )

    result = intent_clarity_and_confirmation.run()

    assert isinstance(result, StageOneResult)
    assert result.intent_confirmation == "Yes"
    assert result.response == ""
    assert result.user_requirements == extracted_dict


def test_stage1_with_no_intent_confirmation(
    intent_clarity_and_confirmation, mock_chat_model
):
    tool_response = [
        {
            "tool_calls": [{"type": "test_tool", "function": {"arguments": {}}}],
            "id": "tool_id_1",
            "content": {"feature": "value"},
        }
    ]

    main_response = [""]
    intent_confirmation = ["No"]
    extracted_dict = {}

    mock_chat_model.get_session_response.side_effect = [tool_response, main_response]
    intent_clarity_and_confirmation._IntentClarityAndConfirmation__intent_confirmation = MagicMock(
        return_value=intent_confirmation
    )
    intent_clarity_and_confirmation._IntentClarityAndConfirmation__extract_dict_from_string = MagicMock(
        return_value=extracted_dict
    )

    result = intent_clarity_and_confirmation.run()

    assert isinstance(result, StageOneResult)
    assert result.intent_confirmation == "No"
    assert result.response == ""
    assert result.user_requirements == extracted_dict
