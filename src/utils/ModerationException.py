class ModerationException(Exception):
    """This is a custom exception class to handle moderation related exceptions"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
