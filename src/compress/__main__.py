import argparse
from pathlib import Path

from .main import with_pool


def existing_dir(path_str: str):
    path = Path(path_str)
    if not path.exists() or not path.is_dir():
        raise argparse.ArgumentTypeError
    return path.absolute()


def dir_with_existing_parent(path_str: str):
    path = Path(path_str)
    if not path.parent.exists() or not path.is_dir():
        raise argparse.ArgumentTypeError
    return path.absolute()


parser = argparse.ArgumentParser(description="Сжать файлы в папке")
parser.add_argument(
    "--path",
    type=existing_dir,
    default=Path().absolute(),
    required=False,
    help="путь к папке с фотографиями",
)
parser.add_argument(
    "--result_dir",
    default=Path("compressed").absolute(),
    type=dir_with_existing_parent,
    required=False,
    help="путь к папке с результатом",
)

def main():
    args = parser.parse_args()
    with_pool(
        base_root=args.path,
        result_root=args.result_dir
    )


if __name__ == "__main__":
    main()