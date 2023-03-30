import requests
from bs4 import BeautifulSoup
import csv
import datetime


# Fct pour extraire les infos d'un produit à partir de son url
def extract_product_infos(product_page_url):
    # Requête sur url puis transformation en objet soup
    page = requests.get(product_page_url).content
    soup = BeautifulSoup(page, "html.parser")
    product_infos = {}

    # On parse pour trouver les infos voulues:
    product_infos["product_page_url"] = product_page_url
    product_infos["universal_product_code"] = (
        soup.find("th", string="UPC").find_next("td").string
    )
    product_main_div = soup.find("div", class_="product_main")
    product_infos["title"] = product_main_div.find("h1").string
    product_infos["price_including_tax"] = (
        soup.find("th", string="Price (incl. tax)").find_next("td").string
    )
    product_infos["price_excluding_tax"] = (
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


# Enregistrer les infos d'un produit dans un .csv
def save_product_infos(product_infos, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(product_infos.keys())
        writer.writerow(product_infos.values())


# Fct pour extraire une liste des produits d'une catégorie donnée par son url
def extract_whole_category(category_index_url, products_links=[]):
    page = requests.get(category_index_url).content
    soup = BeautifulSoup(page, "html.parser")
    # products_links = []
    site_root = "http://books.toscrape.com/catalogue/"
    # Les liens voulus sont tous dans des <h3>:
    products_list_raw = soup.select("h3 a")
    # Liste des liens absolus à partir de la liste en relatifs
    for link in products_list_raw:
        products_links.append(link.get("href").replace("../../../", site_root))

    # On vérifie s'il y a d'autres pages dans la catégorie
    check_next = soup.find("li", class_="next")
    if check_next:
        current_url_suffixe = category_index_url.split("/")[-1]
        next_url_suffixe = check_next.find_next("a").get("href")
        next_url = category_index_url.replace(current_url_suffixe, next_url_suffixe)
        # Le cas échéant on rappelle la fonction récursivement
        return extract_whole_category(next_url, products_links)
    else:
        return products_links


# Enregistrer les infos produits de toute une catégorie en .csv
def save_category_books_infos(products_infos, filename):
    with open(filename, "w", newline="") as file:
        headers = [
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
        ]
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for product_infos in products_infos:
            writer.writerow(product_infos)


# Récupérer une liste des liens de toutes les catégories
def extract_all_categories(website_url):
    page = requests.get(website_url).content
    soup = BeautifulSoup(page, "html.parser")
    categories_anchors = soup.find("ul", class_="nav-list").find_all("a")
    categories_links = []
    link_prefix = "http://books.toscrape.com/"
    for anchor in categories_anchors:
        link = link_prefix + anchor.get("href")
        categories_links.append(link)
    del categories_links[0]  # Le premier lien est une catégorie générique
    return categories_links


""" # Test non intéractif de la phase 1
book_infos = extract_product_infos(
    "http://books.toscrape.com/catalogue/the-requiem-red_995/index.html"
)
# Variable pour nommer les .csv
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = book_infos["title"].replace(" ", "_") + "_" + date_time + ".csv"
save_product_infos(book_infos, filename)

# Test non intéractif de la phase 2
category_url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
books_links = []
# Une liste de tous les liens d'une catégorie définie
books_links = extract_whole_category(category_url, books_links)

# On boucle dessus en utilisant la fonction d'extraction d'infos produits
books_category_infos = []
for book_link in books_links:
    books_category_infos.append(extract_product_infos(book_link))

# Et maintenant on enregistre cette liste de dictionnaires dans un .csv
date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
current_category = books_category_infos[0]["category"]
filename = current_category + "_" + date_time + ".csv"
save_category_books_infos(books_category_infos, filename) """

# Test phase 3: on boucle sur la phase 2

