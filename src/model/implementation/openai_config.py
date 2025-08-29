import os

from dotenv import load_dotenv


class OpenAIConfig:
    def __init__(self):
        pass

    def load_openai_key(self):
        load_dotenv()
        try:
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        except Exception as e:
            raise e
