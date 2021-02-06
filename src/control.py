import sys
from os.path import abspath, dirname, join
from typing import List
from PySide6 import QtCore
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType

from core.qmlcore import Backend
from core.core2 import CoreApp
from core.config import Config
from util.fs import iter_files
from pathlib import Path


def main(argv: List[str]):
    config = Config(Path(argv[1]))

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Instance of the Python object
    backend = Backend(CoreApp(iter_files(Path('.')), config.root_folder, config.root_category))

    # Expose the Python object to QML
    context = engine.rootContext()
    context.setContextProperty("backend", backend)

    #qmlRegisterType(Test, 'TestTypes', 1, 0, 'Test')

    # Get the path of the current directory, and then add the name
    # of the QML file, to load it.
    qmlFile = join(dirname(__file__), 'qml', 'main.qml')
    engine.load(abspath(qmlFile))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
