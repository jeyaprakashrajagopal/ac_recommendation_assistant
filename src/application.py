class Application:
    """Base class where pipeline gets injected and accessed in main file."""

    def __init__(self, pipeline):
        self.pipeline = pipeline
