"""This module contains the Category class."""
from .book import Book


class Category:
    """A Category has a URL and a list of Books."""
    def __init__(self, url: str):
        self.url = url
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def __str__(self):
        return f"Category's URL: {self.url}"
