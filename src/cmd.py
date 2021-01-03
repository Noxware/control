from core.config import config, Category
from core.core import run_base, AskContext
from util.fs import iter_files
from typing import List
from pathlib import Path
from core.core2 import CoreApp


def choose(context: AskContext, options: List[Category]) -> Category:
    print(f'Target: {context.file.name}\n')

    for i, o in enumerate(options):
        print(f'{i} - {o.name}')

    print('')
    selected = input('> ')
    print('')
    return options[int(selected)]


def main():
    backend = CoreApp(iter_files(Path('.')), config.root_folder, config.root_category)
    while True:
        snapshot = backend.wait_for_snapshot()
        if snapshot is None:
            break
        else:
            print(f'Target: {snapshot.file.name}\n')

            for i, o in enumerate(snapshot.options):
                print(f'{i} - {o.name}')

            print('')
            selected = input('> ')
            print('')
            backend.select(snapshot.options[int(selected)])


if __name__ == '__main__':
    main()