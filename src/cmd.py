from core.config import config, Category
from core.core import run_base, AskContext
from util.fs import iter_files
from typing import List
from pathlib import Path


def choose(context: AskContext, options: List[Category]) -> Category:
    print(f'Target: {context.file.name}\n')

    for i, o in enumerate(options):
        print(f'{i} - {o.name}')

    print('')
    selected = input('> ')
    print('')
    return options[int(selected)]


def main():
    run_base(iter_files(Path('.')), config.root_folder, config.root_category, choose)


if __name__ == '__main__':
    main()