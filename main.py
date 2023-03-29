import requests
from bs4 import BeautifulSoup
import csv
import datetime

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
    product_main_div = soup.find("div", class_="product_main")
    product_infos["title"] = product_main_div.find("h1").string
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
    product_infos["review_rating"] = product_main_div.find("p", class_="star-rating")[
        "class"
    ][1]
    product_infos["image_url"] = (
        soup.select_one("div.item.active").find("img").get("src")
    )
    return product_infos


# Enregistrer les infos dans un .csv
def save_product_infos(product_infos, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(product_infos.keys())
        writer.writerow(product_infos.values())


book_infos = extract_product_infos(
    "http://books.toscrape.com/catalogue/the-requiem-red_995/index.html"
)
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = book_infos["title"].replace(" ", "_") + "_" + date_time + ".csv"
save_product_infos(book_infos, filename)
