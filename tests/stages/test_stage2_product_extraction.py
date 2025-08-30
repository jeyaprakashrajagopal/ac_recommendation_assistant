from unittest.mock import call, create_autospec

from src.model.interfaces.chat_model_interface import ChatModel
from src.stages.stage2_product_extraction import (
    ProductExtractionAndMapping,
    StageTwoResult,
)


def test_stage_2_calls_intent_confirmation_with_expected_messages():
    chat_model = create_autospec(ChatModel, instance=True)
    system_message = "Extract products and dictionary from map"
    FAKE_RESPONSE = {
        "cooling capacity": "standard",
        "energy efficiency": "premium",
        "comfort": "essential",
        "portability": "essential",
        "ac type": "standard",
        "smart features": "premium",
    }
    DATABASE_RETRIEVAL = '[{"brand":"Lloyd","model_name":"1.5 Ton 3 Star Inverter Split AC","room_size":18,"capacity_ton":1.5,"energy_efficiency":3,"inverter":"Yes","operating_range":"18\\u201345 \\u00b0C","installation_required":"Yes","delivery_duration":"3\\u20135 days","ac_type":"Split","smart_features":"4\\u2011Way Swing","noise_levels":"36 dB","stars":4.6,"price":43110,"warranty":"1 Year Comprehensive, 10 Years Compressor","portability":"Fixed","description":"Price \\u20b943110: Lloyd 1.5 Ton 3 Star Inverter Split AC offers a cooling capacity of 1.5 Ton for ~18 m\\u00b2 rooms. Energy efficiency is 3-Star with inverter compression, and portability is \'Fixed\' for the Split form factor. Comfort is moderately quiet at around 36 dB. Smart features: 4\\u2011Way Swing. Ideal for Indian summers with an operating range of 18\\u201345 \\u00b0C."},{"brand":"Samsung","model_name":"1.0 Ton 3 Star Inverter Split AC","room_size":12,"capacity_ton":1.0,"energy_efficiency":3,"inverter":"Yes","operating_range":"16\\u201352 \\u00b0C","installation_required":"Yes","delivery_duration":"3\\u20135 days","ac_type":"Split","smart_features":"Wi\\u2011Fi + Voice","noise_levels":"41 dB","stars":4.4,"price":43300,"warranty":"2 Years Product, 10 Years Compressor","portability":"Fixed","description":"Price \\u20b943300: Samsung 1.0 Ton 3 Star Inverter Split AC offers a cooling capacity of 1.0 Ton for ~12 m\\u00b2 rooms. Energy efficiency is 3-Star with inverter compression, and portability is \'Fixed\' for the Split form factor. Comfort is moderately quiet at around 41 dB. Smart features: Wi\\u2011Fi + Voice. Ideal for Indian summers with an operating range of 16\\u201352 \\u00b0C."}]'
    fake_response = StageTwoResult(recommendations=DATABASE_RETRIEVAL)

    chat_model.preview_response.return_value = FAKE_RESPONSE
    stage_2 = ProductExtractionAndMapping(
        chat_model=chat_model, system_message=system_message
    )

    actual = stage_2.run(
        user_requirement={
            "price": 45000,
            "cooling capacity": "standard",
            "energy efficiency": "premium",
            "comfort": "essential",
            "portability": "essential",
            "ac type": "standard",
            "smart features": "premium",
        }
    )
    print("tested ", actual)
    assert actual == fake_response
