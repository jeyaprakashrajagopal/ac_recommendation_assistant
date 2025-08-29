from typing import Dict


def compare_products(user_requirements: Dict, from_dataset: Dict) -> int:
    mapping = {"essential": 0, "standard": 1, "premium": 2}

    score = 0

    for key, value in from_dataset.items():
        user_value = mapping.get(user_requirements[key], -1)
        dataset_value = mapping.get(value, -1)

        if (dataset_value != -1 and user_value != -1) and dataset_value >= user_value:
            score += 1

    return score
