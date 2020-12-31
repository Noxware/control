from core.config import config
from util.fs import make_category


def main():
    make_category(config.root_category, config.root_folder.parent)


if __name__ == '__main__':
    main()