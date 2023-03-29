import requests
from bs4 import BeautifulSoup

# import csv


# Extraire les infos produits à partir de son url
def extract_product_infos(product_page_url):
    # Requête sur url puis transformation en objet soup
    page = requests.get(product_page_url).content
    soup = BeautifulSoup(page, "html.parser")
    product_infos = {}

    # On parse pour trouver les infos voulues:
    # product_infos["product_page_url"] = product_page_url
    product_infos["universal_product_code"] = (
        soup.find("th", string="UPC").find_next("td").string
    )
    product_infos["title"] = soup.find("div", class_="product_main").find("h1").string
    product_infos["price_including_tax"] = (
        soup.find("th", string="Price (incl. tax)").find_next("td").string
    )
    product_infos["price_exluding_tax"] = (
        soup.find("th", string="Price (excl. tax)").find_next("td").string
    )
    product_infos["number_available"] = (
        soup.find("th", string="Availability").find_next("td").string
    )
    product_infos["product_description"] = (
        soup.find("div", id="product_description").find_next("p").string
    )
    # La catégorie arrive toujours après Books dans la liste de navigation:
    product_infos["category"] = (
        soup.find("a", href="../category/books_1/index.html").find_next("a").string
    )

    return product_infos


""" book_infos = extract_product_infos(
    "http://books.toscrape.com/catalogue/the-requiem-red_995/index.html"
)
print(book_infos["category"]) """
