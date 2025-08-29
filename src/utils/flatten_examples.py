import json
from typing import Dict, List


def flatten_examples(path) -> List[Dict]:
    """
    This method reads list of example dictionary from the json file and flattens it so that it can be directly added to llm.

    :param path: str: Path of the few shot examples file
    :return List[Dict]: returns the list of dictionaries with assistant and user dictionaries.
    """
    with open(path, "r") as f:
        examples = json.load(f)

    return [message for example in examples for message in example["messages"]]
