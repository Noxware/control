# Imports
from core.core import Category
from pathlib import Path
from typing import Any, Dict
import yaml


# Errors
class ConfigError(Exception):
    pass

# Classes

class Config:
    def __init__(self, f: Path):
        raw_config: Dict[str, Any] = yaml.safe_load(f.read_text())

        #self.src_folder: Path = Path(__file__).parent.parent
        #self.project_folder = self.src_folder.parent
        self.config_file_folder: Path = f.parent
        self.root_folder: Path = Path(raw_config['config']['root_folder'])

        if not self.root_folder.is_absolute():
            self.root_folder = self.config_file_folder / self.root_folder

        self.root_category: Category = Category(self.root_folder.name, raw_config['root'])