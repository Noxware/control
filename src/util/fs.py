from util.config import Category
from pathlib import Path


def make_category(cat: Category, place: Path) -> None:

    this_path = place / cat.name
    this_path.mkdir(parents=True, exist_ok=True)

    if cat.children is not None:
        for n, c in cat.children.items():
            if c is None:
                (this_path / n).mkdir(parents=True, exist_ok=True)
            else:
                make_category(c, this_path)


# def filename_split_int(fn: str)


def safe_name(p: Path):
    pass


def safe_move(source: Path, target: Path):
    pass


def list_files(folder: Path):
    for p in folder.iterdir():
        if p.is_file():
            yield p