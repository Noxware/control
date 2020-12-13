# Imports
import yaml
from pathlib import Path
from typing import Mapping, Any, Optional


# Errors
class ConfigError(Exception):
    pass


# Constants
defaults = None

# Classes
class Category:
    question: str
    omit: bool
    self_included: bool
    transparent: bool
    ignored: bool
    hint: Optional[str]

    def __init__(self):
        pass


# Code
config_path: Path = None
raw_config: Mapping[Any, Any] = None
config = None


def init():
    global raw_config

    try:
        if Path('custom2.yaml').is_file():
            config_path = Path('custom2.yaml')
        else:
            config_path = Path('custom.yaml')

        raw_config = yaml.safe_load(config_path.read_text())
    except Exception:
        raise ConfigError("Error loading 'custom.yaml'.")


init()