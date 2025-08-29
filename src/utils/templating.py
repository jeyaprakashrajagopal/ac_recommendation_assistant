import ast
from pathlib import Path


def load_system_message(template_path: str, **params):
    """
    Reads the markdown template and renders it with named placeholders.

    :param template_path str: Path of the MD file
    :param **params str: Positional parameters that can be embedded into the system message
    """
    path = Path(template_path)
    system_message = path.read_text(encoding="utf-8")
    try:
        return system_message.format(**params)
    except KeyError as key_error:
        missing = key_error.args
        raise KeyError(f"Missing template parameter: '{missing}' for {path}")


def load_system_message_without_params(template_path: str):
    """
    Reads the markdown template and renders it.

    :param template_path str: Path of the MD file
    """
    path = Path(template_path)
    return path.read_text("utf-8")


def load_dictionary_from_md(template_path: str):
    """
    Reads the markdown template and renders it.

    :param template_path str: Path of the MD file
    """
    with open(template_path) as data:
        return ast.literal_eval(data.read())
