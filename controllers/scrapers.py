"""Functions related to scraping data from the web."""

import requests
from bs4 import BeautifulSoup
from models.book import Book
from helpers import get_first_number


def make_soup(url: str) -> BeautifulSoup:
    """
    Takes an URL and returns a BeautifulSoup object.
    """
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html.parser")
    return soup


def scrape_book_infos(book_url: str) -> Book:
    """Takes a book URL and returns a Book object."""
    soup = make_soup(book_url)
    book = Book(book_url)

    # Now we scrape the book infos
    upc = soup.find("th", string="UPC")
    book.upc = (
        upc.find_next("td").string if upc else "Missing data"
    )
    product_main_div = soup.find("div", class_="product_main")
    title = product_main_div.find("h1")
    book.title = title.string if title else "Missing data"
    price_incl_tax = soup.find("th", string="Price (incl. tax)")
    book.price_incl_tax = (
        price_incl_tax.find_next("td").string if price_incl_tax else "Missing data"
    )
    price_excl_tax = soup.find("th", string="Price (excl. tax)")
    book.price_excl_tax = (
        price_excl_tax.find_next("td").string if price_excl_tax else "Missing data"
    )
    availability = soup.find("th", string="Availability")
    if availability:
        availability_str = availability.find_next("td").string
        book.number_available = str(get_first_number(availability_str))
    else:
        book.number_available = "Missing data"

    product_description = soup.find("div", id="product_description")
    if product_description:
        book.product_description = product_description.find_next("p").string
    else:
        book.product_description = "Missing data"
    category = soup.find("a", href="../category/books_1/index.html")
    book.category = (
        category.find_next("a").string if category else "Missing data"
    )
    star_rating = product_main_div.find("p", class_="star-rating")
    book.review_rating = (
        star_rating["class"][1] if star_rating else "Missing data"
    )

