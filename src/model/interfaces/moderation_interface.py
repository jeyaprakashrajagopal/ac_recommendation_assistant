from abc import ABC, abstractmethod


class Moderation(ABC):
    @abstractmethod
    def get_response(self, input_message) -> bool:
        """
        :param str input_message: moderation check on the given message
        :return: returns True if there is a sensitive content
        """
        pass
