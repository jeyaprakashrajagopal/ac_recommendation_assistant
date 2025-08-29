import pytest

from src.stages.compare_products import compare_products


def test_no_requirements_met():
    user = {
        "cooling capacity": "standard",
        "energy efficiency": "standard",
        "comfort": "premium",
        "portability": "premium",
        "ac type": "premium",
        "smart features": "premium",
    }
    dataset = {
        "cooling capacity": "essential",
        "energy efficiency": "essential",
        "comfort": "essential",
        "portability": "essential",
        "ac type": "standard",
        "smart features": "essential",
    }

    assert compare_products(user_requirements=user, from_dataset=dataset) == 0


def test_all_requirements_met():
    user = {
        "cooling capacity": "essential",
        "energy efficiency": "essential",
        "comfort": "essential",
        "portability": "essential",
        "ac type": "standard",
        "smart features": "essential",
    }
    dataset = {
        "cooling capacity": "standard",
        "energy efficiency": "standard",
        "comfort": "premium",
        "portability": "essential",
        "ac type": "standard",
        "smart features": "premium",
    }

    assert compare_products(user_requirements=user, from_dataset=dataset) == 6


def test_four_requirements_met():
    user = {
        "cooling capacity": "essential",
        "energy efficiency": "essential",
        "comfort": "premium",
        "portability": "essential",
        "ac type": "premium",
        "smart features": "essential",
    }
    dataset = {
        "cooling capacity": "standard",
        "energy efficiency": "standard",
        "comfort": "essential",
        "portability": "essential",
        "ac type": "standard",
        "smart features": "premium",
    }

    assert compare_products(user_requirements=user, from_dataset=dataset) == 4


def test_missing_keys_in_dataset():
    user = {"cooling capacity": "standard", "energy efficiency": "standard"}
    dataset = {"cooling capacity": "standard"}

    assert compare_products(user_requirements=user, from_dataset=dataset) == 1


def test_missing_dataset():
    user = {
        "cooling capacity": "essential",
        "energy efficiency": "essential",
        "comfort": "premium",
        "portability": "essential",
        "ac type": "premium",
        "smart features": "essential",
    }
    dataset = {}

    assert compare_products(user_requirements=user, from_dataset=dataset) == 0


def test_missing_both_user_requirement_and_in_dataset():
    user = {}
    dataset = {}

    assert compare_products(user_requirements=user, from_dataset=dataset) == 0


def test_missing_values_in_dataset():
    user = {
        "cooling capacity": "",
        "energy efficiency": "",
        "comfort": "",
        "portability": "essential",
        "ac type": "premium",
        "smart features": "essential",
    }
    dataset = {
        "cooling capacity": "essential",
        "energy efficiency": "essential",
        "comfort": "premium",
        "portability": "standard",
        "ac type": "standard",
        "smart features": "essential",
    }

    assert compare_products(user_requirements=user, from_dataset=dataset) == 5


def test_missing_values_in_dataset():
    user = {
        "cooling capacity": "essential",
        "energy efficiency": "essential",
        "comfort": "premium",
        "portability": "standard",
        "ac type": "standard",
        "smart features": "essential",
    }
    dataset = {
        "cooling capacity": "",
        "energy efficiency": "",
        "comfort": "",
        "portability": "essential",
        "ac type": "premium",
        "smart features": "essential",
    }

    assert compare_products(user_requirements=user, from_dataset=dataset) == 2


def test_unknown_values_in_dataset():
    user = {
        "cooling capacity": "standard",
        "energy efficiency": "standard",
        "portability": "unknown",
    }
    dataset = {
        "cooling capacity": "premium",
        "energy efficiency": "unknown",
        "portability": "unknown",
    }

    assert compare_products(user_requirements=user, from_dataset=dataset) == 1
