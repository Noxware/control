from pathlib import Path
from typing import Iterable, Callable, List, Optional, Dict, Any
from util.fs import safe_move


class CoreException(Exception):
    """Exception returned from this particular module"""
    pass


class Category:
    def __init__(self, name: str, raw_category: Optional[Dict[str, Any]]):
        rc = raw_category.copy() if raw_category is not None else {}

        self.name: str = name
        self.question: str = rc.pop('__question', 'How would you classify this?')
        self.omit: bool = rc.pop('__omit', True)
        self.self_included: bool = rc.pop('__self', True)
        self.transparent: bool = rc.pop('__transparent', False)
        self.ignored: bool = rc.pop('__ignored', False)
        self.hint: Optional[str] = rc.pop('__hint', None)
        self.children: Optional[Dict[str, Category]] = None

        for key in list(rc.keys()):
            if key.startswith('__'):
                rc.pop(key)

        if len(rc) > 0:
            self.children = {}
            for key, value in rc.items():
                self.children[key] = Category(key, value)


class AskContext:
    def __init__(self, file: Path, question: str, self_included: bool, category: Optional[Category]):
        self.file = file
        self.question = question
        self.self_included = self_included
        self.category = category


def cats2path(cats: Iterable[Category]) -> Path:
    """Takes a list of Category and returns a path to the folder"""
    res = None

    for c in cats:
        if res is None:
            res = Path(c.name)
        else:
            res = res / Path(c.name)

    if res is None:
        raise CoreException('Can not get items from the iterable [cats]')

    return res


def make_category(cat: Category, place: Path) -> None:
    this_path = place / cat.name
    this_path.mkdir(parents=True, exist_ok=True)

    if cat.children is not None:
        for n, c in cat.children.items():
            if c is None:
                (this_path / n).mkdir(parents=True, exist_ok=True)
            else:
                make_category(c, this_path)


TransparencyTable = Dict[Category, Category]


def flat_transparency(cat: Category) -> Optional[TransparencyTable]:
    """
    Returns a transparency table or None if [cat] is not transparent.
    A transparency table maps children (cc) of the transparent parent [cat] (ct) to ct.
    If children (ch) is transparent, the children (cc) of ch is mapped to ch, and ch to ct.

    cc1 -> ct
    cc2 -> ct
    cc3 -> ct
    ---
    ch  -> ct
    cc4 -> ch
    cc5 -> ch

    :param cat: Any category transparent or not
    :return: Transparency table, or None if not transparent
    """

    if not cat.transparent:
        return None
    else:
        # Maps A children to its transparent parent
        transparency_table: TransparencyTable = {}
        for c in cat.children.values():
            # Any child is a transparent child of its parent so it must be in the table
            transparency_table[c] = cat
            # Try to get a transparency table from this child
            child_table = flat_transparency(c)
            if child_table is not None:
                # Merge the transparency tables. Example:
                # ct: transparent parent, cc: child, ch: both
                #
                # cc1 -> ct
                # cc2 -> ct
                # ch -> ct
                # cc3 -> ch
                transparency_table = {**transparency_table, **child_table}

        return transparency_table


CategoryPath = List[Category]


def resolve_transparency(cat: Category, table: TransparencyTable) -> CategoryPath:
    """
    This utility function is used to get the full CategoryPath of a selected transparent child.

    :param cat:
    :param table:
    :return:
    """
    if cat not in table:
        return [cat]
    else:
        return [*resolve_transparency(table[cat], table), cat]


ChooseFunction = Callable[[AskContext, List[Category]], Category]


def ask_single(file: Path, cat: Category, choose: ChooseFunction) -> CategoryPath:
    """
    Generic algorithm builds the path of categories. It needs a choose function to ask
    the user. The function must list the categories in the second parameter but it also
    needs to take care of 'question' and 'self_included' in context.

    Transparency and other things are automatically handled if you use this function.


    :param file:
    :param cat:
    :param choose:

    :return: Category path
    """

    t_table: TransparencyTable = {}
    choose_from: List[Category] = []
    assert cat.children is not None

    for c in cat.children.values():
        c_table = flat_transparency(c)
        if c_table is None:
            choose_from.append(c)
        else:
            t_table = {**t_table, **c_table}
            for c2 in t_table.keys():
                # Sub transparent categories are part of the table
                if not c2.transparent:
                    choose_from.append(c2)

    selected = choose(AskContext(file, cat.question, cat.self_included, cat), choose_from)
    return resolve_transparency(selected, t_table)


def ask_full(file: Path, cat: Category, choose: ChooseFunction) -> CategoryPath:
    selected_path = ask_single(file, cat, choose)
    if selected_path[-1].children is None:
        return selected_path
    else:
        return [*selected_path, *ask_full(file, selected_path[-1], choose)]


def organize(file: Path, root_folder: Path, cats: CategoryPath) -> None:
    """Move a file into the category folder"""
    target_folder = cats2path(cats)
    safe_move(file, root_folder / target_folder / file.name)


def run_base(files: Iterable[Path], root_folder: Path, root_cat: Category, choose: ChooseFunction) -> None:
    make_category(root_cat, root_folder.parent)
    for f in files:
        cat_path = ask_full(f, root_cat, choose)
        organize(f, root_folder, cat_path)