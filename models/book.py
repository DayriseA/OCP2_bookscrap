"""This module contains the Book class."""


class Book:
    """Books have infos we want to scrape and store"""

    def __init__(
        self,
        url,
        upc="",
        title="",
        price_incl_tax="",
        price_excl_tax="",
        number_available="",
        product_description="",
        category="",
        review_rating="",
        image_url="",
    ):
        self.url = url
        self.upc = upc
        self.title = title
        self.price_incl_tax = price_incl_tax
        self.price_excl_tax = price_excl_tax
        self.number_available = number_available
        self.product_description = product_description
        self.category = category
        self.review_rating = review_rating
        self.image_url = image_url

    def __str__(self):
        return f"Book: {self.title} - {self.category}"
