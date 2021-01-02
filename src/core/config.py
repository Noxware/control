# Imports
from core.core import Category
from pathlib import Path
from typing import Any, Dict
import yaml


# Errors
class ConfigError(Exception):
    pass

# Types

# Constants


# Classes



class Config:
    def __init__(self, raw_config: Dict[str, Any]):
        self.src_folder: Path = Path(__file__).parent.parent
        self.project_folder = self.src_folder.parent
        self.root_folder: Path = Path(raw_config['config']['root_folder'])

        if not self.root_folder.is_absolute():
            self.root_folder = self.project_folder / self.root_folder

        self.root_category: Category = Category(self.root_folder.name, raw_config['root'])


# Code
config: Config


def init() -> None:
    global config

    config_file: Path
    raw_config: Dict[str, Any]
    config_folder: Path = Path(__file__).parent.parent / 'config'

    try:
        if (config_folder / 'custom2.yaml').is_file():
            config_file = config_folder / 'custom2.yaml'
        else:
            config_file = config_folder / 'custom.yaml'

        raw_config = yaml.safe_load(config_file.read_text())
        config = Config(raw_config)

    except Exception:
        raise ConfigError("Error loading 'custom.yaml'.")


def reload_config() -> None:
    init()


init()