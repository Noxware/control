from PySide6.QtCore import QObject, Signal, Property, QUrl, Slot
from core.core import Category
from core.core2 import CoreApp, Snapshot
from typing import List, Optional, Dict
from pathlib import Path
import os
import sys

file_types = {
    'image': [
        'jpg',
        'jpeg',
        'bmp',
        #'gif',
        #'webp',
        'png',
    ],
    'video': [
        'mp4',
        'avi',
        'wmv',
        'mkv',
    ],
    'text': [
        'txt',
        'py',
        'js',
        'md',
        'dart',
        'html',
        'css',
        'bat',
        'vbs',
    ]
}

class Backend(QObject):
    def __init__(self, app_core: CoreApp):
        QObject.__init__(self, None)  # parent null args removed
        self.app_core = app_core
        self.optionsMap: Dict[str, Category] = {}

    @Slot(result='QVariant')
    def wait_for_snapshot(self):
        snap = self.app_core.wait_for_snapshot()
        if snap is None:
            return None

        for o in snap.options:
            self.optionsMap[o.name] = o  # possible future bug if names repeated

        return snap.to_dict()

    @Slot(str)
    def select(self, cat_name: str):
        self.app_core.select(self.optionsMap[cat_name])
        self.optionsMap.clear()  # Necessary?

    @Slot(str, result=str)
    def get_file_type(self, f):
        p = Path(f)
        s = p.suffix[1:].lower()

        if s in file_types['image']:
            return 'image'
        elif s in file_types['video']:
            return 'video'
        elif s in file_types['text']:
            return 'text'
        else:
            return 'file'

    @Slot(str)
    def view_external_file(self, f):
        p = sys.platform

        if p == 'win32':
            os.startfile(f)
        elif p == 'darwin':
            pass
        else:
            pass

    @Slot(str, result='QUrl')
    def url_from_file(self, f):
        return QUrl.fromLocalFile(f)

    @Slot(str, result=str)
    def get_file_content(self, f):
        return Path(f).read_text()