import sys
from os.path import abspath, dirname, join
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from core.qmlcore import Backend, CategoryWrapper
from core.core import run_base
from core.config import config
from util.fs import iter_files
from pathlib import Path


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Instance of the Python object
    backend = CategoryWrapper(config.root_category)

    # Expose the Python object to QML
    context = engine.rootContext()
    context.setContextProperty("backend", backend)

    # Get the path of the current directory, and then add the name
    # of the QML file, to load it.
    qmlFile = join(dirname(__file__), 'qml', 'main.qml')
    engine.load(abspath(qmlFile))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
