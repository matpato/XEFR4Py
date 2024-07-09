import pathlib
import re
import sys


def get_list_from_str(list_str: str) -> list[str]:
    """
    Convert a string to a list of strings
    :param list_str: string with list format
    :return: the list from the string
    """
    return re.findall("\\b[^\"'[\],]+", list_str)


def get_plain_str_from_list(lst: list[str]) -> str:
    """
    Convert a list of strings to a string
    :param lst: list of strings
    :return: the string from the list
    """
    return str(lst)[1:-1]


def get_log_dir() -> str:
    home: pathlib.Path = pathlib.Path.home()

    appdata: pathlib.Path

    if sys.platform == "win32":
        appdata = home / "AppData/Roaming"
    elif sys.platform == "linux":
        appdata = home / ".local/share"
    elif sys.platform == "darwin":
        appdata = home / "Library/Application Support"
    return str(appdata / 'xefr4py_logs')
