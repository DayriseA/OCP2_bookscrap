"""This module contains the Website class."""


class Website:
    """The website to be scrapped. Has a url and a list of categories URLs"""

    def __init__(self, url: str):
        """Initialize the website with the url."""
        self.url = url
        self.categories_urls = []

    def add_category_url(self, category_url: str):
        """Add a category url to the list of categories URLs."""
        self.categories_urls.append(category_url)

    def __str__(self):
        return f"Website's URL: {self.url}"
