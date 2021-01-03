from typing import Iterable, List, Optional
from pathlib import Path
from core.core import Category, AskContext, run_base
from threading import Thread, Event


class RunBaseWrapper(Thread):
    def __init__(self, files: Iterable[Path], root_folder: Path, root_cat: Category):
        super(RunBaseWrapper, self).__init__(daemon=True)
        self.files = files
        self.root_folder = root_folder
        self.root_cat = root_cat

        self.snapshot: Optional[Snapshot] = None
        self.snapshot_ready = Event()
        self.answer: Optional[Category] = None
        self.answered = Event()

    def select(self, selected: Category):
        self.answer = selected
        self.snapshot_ready.clear()
        self.answered.set()

    def wait_for_snapshot(self) -> Optional['Snapshot']:
        self.snapshot_ready.wait()
        return self.snapshot

    def choose(self, context: AskContext, options: List[Category]) -> Category:
        self.snapshot = Snapshot(context.file, context.question, context.self_included, context.category, options)
        self.snapshot_ready.set()

        self.answered.clear()
        self.answered.wait()

        # self.snapshot_ready.clear()

        assert self.answer is not None
        return self.answer

    def run(self):
        run_base(self.files, self.root_folder, self.root_cat, self.choose)
        self.snapshot = None
        self.snapshot_ready.set()


class Snapshot:
    def __init__(self,
                 file: Path,
                 question: str,
                 self_included: bool,
                 category: Category,
                 options: List[Category]):

        self.file = file
        self.question = question
        self.self_included = self_included
        self.category = category
        self.options = options

    def to_dict(self):
        return {
            'file': str(self.file.absolute()),  # Fix?
            'question': self.question,
            'self_included': self.self_included,
            'category': self.category.to_dict(),
            'options': [c.to_dict() for c in self.options]
            ###
        }


class CoreApp:
    def __init__(self, files: Iterable[Path], root_folder: Path, root_cat: Category):
        self.files = files
        self.root_folder = root_folder
        self.root_cat = root_cat

        self.base_runner = RunBaseWrapper(files, root_folder, root_cat)
        self.base_runner.start()

    def wait_for_snapshot(self) -> Optional[Snapshot]:
        return self.base_runner.wait_for_snapshot()

    def select(self, cat: Category) -> None:
        self.base_runner.select(cat)
