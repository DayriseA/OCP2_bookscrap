"""Utility functions."""

import re


def get_first_number(string: str) -> int:
    """
    Takes a string and returns the first number found in it.
    Returns none if no number is found.
    """
    match = re.search(r"\d+", string)
    return int(match.group()) if match else None
