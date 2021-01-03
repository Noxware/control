from PySide6.QtCore import QObject, Signal, Property, QUrl, Slot
from core.core import Category
from core.core2 import CoreApp, Snapshot
from typing import List, Optional


class CategoryWrapper(QObject):
    def __init__(self, cat: Category):
        QObject.__init__(self, None)

        self.m_name = cat.name
        self.m_question = cat.question
        self.m_self_included = cat.self_included
        self.m_hint = cat.hint
        self.m_ignored = cat.ignored

        self.category = cat

    name_changed = Signal(str)
    question_changed = Signal(str)
    self_included_changed = Signal(bool)
    hint_changed = Signal(str)
    ignored_changed = Signal(bool)

    @Property(str, notify=name_changed)
    def name(self):
        return self.m_name

    @name.setter
    def name(self, n: str):
        if self.m_name != n:
            self.m_name = n
            self.name_changed.emit(n)

    @Property(str, notify=question_changed)
    def question(self):
        return self.m_question

    @question.setter
    def question(self, q: str):
        if self.m_question != q:
            self.m_question = q
            self.question_changed.emit(q)
    # @Slot()
    # def test(self):
    #    self.name = 'opaaa'



class SnapshotWrapper(QObject):
    def __init__(self, snapshot: Snapshot):
        QObject.__init__(self, None)

        self.m_file = str(snapshot.file)
        self.m_question = snapshot.question
        self.m_self_included = snapshot.self_included
        self.m_category = CategoryWrapper(snapshot.category)
        self.m_options = [CategoryWrapper(c) for c in snapshot.options]

    file_changed = Signal(str)
    question_changed = Signal(str)
    self_included_changed = Signal(bool)
    category_changed = Signal(CategoryWrapper)
    options_changed = Signal('QVariantList')

    @Property(str, notify=file_changed)
    def file(self):
        return self.m_file

    @file.setter
    def file(self, f: str):
        if self.m_file != f:
            self.m_file = f
            self.file_changed.emit(f)


    @Property(str, notify=question_changed)
    def question(self):
        return self.m_question

    @question.setter
    def question(self, q: str):
        if self.m_question != q:
            self.m_question = q
            self.question_changed.emit(q)

    @Property(bool, notify=self_included_changed)
    def self_included(self):
        return self.m_self_included

    @self_included.setter
    def self_included(self, s: bool):
        if self.m_self_included != s:
            self.m_self_included = s
            self.self_included_changed.emit(s)

    @Property(CategoryWrapper, notify=category_changed)
    def category(self):
        return self.m_category

    @category.setter
    def category(self, c: CategoryWrapper):
        if self.m_category != c:
            self.m_category = c
            self.category_changed.emit(c)

    @Property('QVariantList', notify=options_changed)
    def options(self):
        return self.m_options

    @options.setter
    def options(self, o: List[CategoryWrapper]):
        if self.m_options != o:
            self.m_options = o
            self.options_changed.emit(o)


class Backend(QObject):
    def __init__(self, app_core: CoreApp):
        QObject.__init__(self, None)  # parent null args removed
        self.app_core = app_core

    @Slot(result=SnapshotWrapper)
    def wait_for_snapshot(self) -> Optional[SnapshotWrapper]:
        return SnapshotWrapper(self.app_core.wait_for_snapshot())

    @Slot(CategoryWrapper)
    def select(self, cat: CategoryWrapper) -> None:
        self.app_core.select(cat.category)