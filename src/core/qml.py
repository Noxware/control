from PySide6.QtCore import QObject, Signal, Property, QUrl, Slot
from core.core import Category, AskContext
from typing import List


class Backend(QObject):
    def __init__(self):
        QObject.__init__(self, None)  # parent null args removed
        self.m_data = {
            # 'context': context.to_dict(),
            # 'categories': [c.to_dict() for c in categories]
            'context': {'aaa': 'bbb'},
        }

    def get_data(self):
        return self.m_data

    def select(self):
        pass

    data = Property('QVariantMap', fget=get_data)
