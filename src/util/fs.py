from pathlib import Path
from datetime import datetime
from base64 import b32encode
from random import randint
from shutil import move
from typing import List, Optional
from fnmatch import fnmatch


class FsException(Exception):
    """Exception returned from this particular module"""
    pass


# def filename_split_int(fn: str)


def encode_int(i: int) -> str:
    """
    B32 based encoding for integers

    :param i: Int to encode
    :return: Encoded string
    """

    return b32encode(i.to_bytes(8, 'big').lstrip(b'\x00')).replace(b'=', b'').lower().decode()


def encoded_time() -> str:
    """Return a rounded timestamp encoded with encode_int() (len 7)"""

    return encode_int(int(datetime.now().timestamp()))


# def encoded_random() -> str:
#    """ Return a random encoded number between 0 and 9999999 (len 5)"""
#
#    return encode_int(randint(0, 9999999))


# def improbable_name() -> str:
#    """Return an improbable name (len 12)"""
#    return encoded_time() + encoded_random()


def safe_path(p: Path) -> Path:
    """
    If the target file already exists, a safe path with other name will be returned.
    Otherwise returns the Path passed as parameter.

    The safe path has a limit of 80 characters.

    :param p: Expected path
    :return: Unique path
    """

    if not p.exists():
        return p
    else:
        name = p.stem
        ext = p.suffix
        improbable = '_' + encoded_time()  # len 8

        # Total filename will have less than 80 chars.
        # 10 is 8 rounded
        max_name_len = 80 - len(ext) - 10
        new_p = p.parent / Path(name[0:max_name_len] + improbable + ext)

        if not new_p.exists():
            return new_p
        else:
            return safe_path(new_p)


def safe_move(source: Path, target: Path) -> None:
    """
    Moves a file using shutil.move(). If the target file already exists
    safe_path() will be used to get a new unique filename. The parent
    folder is created automatically if does not exist.
    """

    target.parent.mkdir(parents=True, exist_ok=True)
    move(source, safe_path(target))

def _matchAny(fname: str, patterns: Optional[List[str]]) -> bool:
    """
    Checks if a filename has a certian unix pattern (case insensitive).
    
    Returns false if patterns is None.
    """
    if patterns is not None:
        for p in patterns:
            if fnmatch(fname, p):
                return True

    return False

def iter_files(folder: Path, exceptions: Optional[List[str]] = None):
    """Only iterates over files in a directory"""
    for p in folder.iterdir():
        if p.is_file() and not _matchAny(p.name, exceptions):
            yield p


#def iter_subfiles(folder: Path):
#    for p in folder.rglob('*'):
#        if p.is_file():
#            yield p