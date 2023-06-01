"""This module contains the Img class."""


class Img:
    """My custom Img class."""

    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return f"Img's URL: {self.url}"
