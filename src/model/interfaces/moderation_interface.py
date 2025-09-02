from abc import ABC, abstractmethod


class Moderation(ABC):
    @abstractmethod
    def get_response(self, input_message) -> bool:
        """
        Invokes OpenAI moderation check API and returns either the message is flagged or not.

        :param str input_message: Input message under check.
        :return bool: returns True if there is a sensitive/violent content, otherwise False
        """
        pass
