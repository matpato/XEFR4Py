import re


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
