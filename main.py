import requests
from bs4 import BeautifulSoup
import csv
import datetime


def extract_product_infos(product_page_url):
    """
    Takes a product url, returns the product informations.

    Parameters:
    product_page_url: str (url)

    Return:
    product_infos: dict of product informations
    """
    # Request the url and make our soup object
    page = requests.get(product_page_url).content
    soup = BeautifulSoup(page, "html.parser")
    product_infos = {}

    # Parsing to find the desired informations
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
    # The category always comes after Books in the navigation list
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


def save_product_infos(product_infos, filename):
    """ Writes the product informations in a csv file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(product_infos.keys())
        writer.writerow(product_infos.values())


def extract_whole_category(category_index_url, products_links=[]):
    """
    Takes a category index url and returns a list of products links.

    Parameters:
    category_index_url: str (url)
    products_links: list of str (url), optional, default empty

    Return:
    products_links: list of str (url)
    """
    page = requests.get(category_index_url).content
    soup = BeautifulSoup(page, "html.parser")
    site_root = "http://books.toscrape.com/catalogue/"
    # Needed anchors are all in <h3> tags
    products_list_raw = soup.select("h3 a")
    # Getting the relatives href and turning them in absolutes ones
    for link in products_list_raw:
        products_links.append(link.get("href").replace("../../../", site_root))

    # Checking if there is a next page in the category
    check_next = soup.find("li", class_="next")
    if check_next:
        current_url_suffixe = category_index_url.split("/")[-1]
        next_url_suffixe = check_next.find_next("a").get("href")
        next_url = category_index_url.replace(current_url_suffixe, next_url_suffixe)
        # If applicable, function is called recursively
        return extract_whole_category(next_url, products_links)
    else:
        return products_links


def save_category_books_infos(products_infos, filename):
    """ Writes the products informations from a whole category in a csv file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
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


def extract_all_categories(website_url):
    """
    Takes the website home page and returns a list of all categories links.

    Parameters:
    website_url: str (url)

    Return:
    categories_links: list of str (url)
    """
    page = requests.get(website_url).content
    soup = BeautifulSoup(page, "html.parser")
    categories_anchors = soup.find("ul", class_="nav-list").find_all("a")
    categories_links = []
    link_prefix = "http://books.toscrape.com/"
    for anchor in categories_anchors:
        link = link_prefix + anchor.get("href")
        categories_links.append(link)
    del categories_links[0]  # First link is a generic one we don't want
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

# Test phase 3: En gros, on boucle sur la phase 2
categories_link = extract_all_categories("http://books.toscrape.com/index.html")

for link in categories_link:
    books_links = []
    books_links = extract_whole_category(link, books_links)
    books_category_infos = []
    for book_link in books_links:
        books_category_infos.append(extract_product_infos(book_link))

    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    current_category = books_category_infos[0]["category"]
    filename = "scrapped_datas/" + current_category + "_" + date_time + ".csv"
    save_category_books_infos(books_category_infos, filename)
    print("Enregistrement de la catégorie " + current_category + " terminé")
