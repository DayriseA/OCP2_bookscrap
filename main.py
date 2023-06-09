import requests
from bs4 import BeautifulSoup
import csv
import datetime
import re
import os


def download_img(img_url, file_path):
    """Takes an image url and download this image to the specified file path."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
    else:
        print("Erreur lors de la récupération de l'image " + img_url)


def extract_product_infos(product_page_url):
    """
    Takes a product url, returns the product informations, download product image.

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
    upc = soup.find("th", string="UPC")
    product_infos["universal_product_code"] = (
        upc.find_next("td").string if upc else "Missing data"
    )
    product_main_div = soup.find("div", class_="product_main")
    title = product_main_div.find("h1")
    product_infos["title"] = title.string if title else "Missing data"
    price_incl_tax = soup.find("th", string="Price (incl. tax)")
    product_infos["price_including_tax"] = (
        price_incl_tax.find_next("td").string if price_incl_tax else "Missing data"
    )
    price_excl_tax = soup.find("th", string="Price (excl. tax)")
    product_infos["price_excluding_tax"] = (
        price_excl_tax.find_next("td").string if price_excl_tax else "Missing data"
    )
    availability = soup.find("th", string="Availability")
    if availability:
        availability_str = availability.find_next("td").string
        availability_int = int(re.findall(r"\d+", availability_str)[0])
        product_infos["number_available"] = availability_int
    else:
        product_infos["number_available"] = "Missing data"

    product_description = soup.find("div", id="product_description")
    if product_description:
        product_infos["product_description"] = product_description.find_next("p").string
    else:
        product_infos["product_description"] = "Missing data"

    category = soup.find("a", href="../category/books_1/index.html")
    product_infos["category"] = (
        category.find_next("a").string if category else "Missing data"
    )
    star_rating = product_main_div.find("p", class_="star-rating")
    product_infos["review_rating"] = (
        star_rating["class"][1] if star_rating else "Missing data"
    )
    img_src = soup.select_one("div.item.active img")
    if img_src:
        img_relative = img_src.get("src")
        img_ext = img_relative[-4:]
        img_url = img_relative.replace("../../", "http://books.toscrape.com/")
        product_infos["image_url"] = img_url
        # Handling some filenames errors with forbidden characters
        purification_table = str.maketrans(
            {
                "\\": "_",
                "/": "_",
                ":": "_",
                "*": "_",
                "?": "_",
                '"': "_",
                "<": "_",
                ">": "_",
                "|": "_",
            }
        )
        img_name = product_infos["title"].translate(purification_table)
        save_path = (
            "scrapped_datas/images/"
            + product_infos["category"]
            + "/"
            + img_name
            + img_ext
        )
        download_img(img_url, save_path)
    else:
        product_infos["image_url"] = "Missing data"

    return product_infos


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


def save_category_books_infos(products_infos, file_path):
    """Writes the products informations from a whole category in a csv file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", newline="", encoding="utf-8") as file:
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


def main():
    """
    This function scrap the books infos we want and their cover image, regrouped
    by categories. Said infos are saved in csv files.
    """
    categories_link = extract_all_categories("http://books.toscrape.com/index.html")
    for link in categories_link:
        books_links = []
        books_links = extract_whole_category(link, books_links)
        books_category_infos = []
        for book_link in books_links:
            books_category_infos.append(extract_product_infos(book_link))
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        current_category = books_category_infos[0]["category"]
        file_path = "scrapped_datas/" + current_category + "_" + date_time + ".csv"
        save_category_books_infos(books_category_infos, file_path)
        print(f"Category {current_category} succesfully recorded in {file_path}")

    print("Task succesfull")


if __name__ == "__main__":
    main()
