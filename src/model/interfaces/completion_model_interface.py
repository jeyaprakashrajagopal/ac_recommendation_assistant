from abc import ABC, abstractmethod
from typing import List


class TextCompletionModel(ABC):
    @abstractmethod
    def get_completion_response(self, prompt: str) -> List[str]:
        """
        To make a single completions request and this is not a chat completion request.

        :param bool json_format: True if response_format is json object False otherwise.
        :return: list of answers
        """
        pass
