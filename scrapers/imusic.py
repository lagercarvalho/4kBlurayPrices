from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import re
from tqdm import tqdm
import json

with open("../config.json", "r") as f:
    config = json.load(f)["imusic"]

url = config["url"]
headers = config["headers"]

home_page = requests.get(url, headers=headers)
home_soup = BeautifulSoup(home_page.text, "html.parser")
form_data = (
    home_soup.find("form", class_="navbar-form navbar-right")
    .get_text(separator=",", strip=True)
    .split(",")[:-1]
)
pages = [list(map(int, page.split("–"))) for page in form_data]
print(f"Importing {pages[-1][-1]} movies")

movies = {"vendor": [], "title": [], "c_price": [], "p_price": [], "sale": []}

enum = enumerate(pages)
if "-v" in sys.argv:
    enum = tqdm(enum, total=len(pages), desc="Processing pages")

for index, page in enum:

    if index != 0:
        index_page = requests.get(f"{url}?offset={page[0]-1}", headers=headers)
        page_soup = BeautifulSoup(index_page.text, "html.parser")
    else:
        page_soup = home_soup

    page_movies = page_soup.find_all("div", class_="list-item")

    for movie in page_movies:
        regex = r"\d+(?:,\d+)?"
        price_text = (
            movie.find("a", class_="price").get_text(strip=True).replace(".", "")
        )
        c_price = float(re.search(regex, price_text).group().replace(",", "."))

        p_price_tag = movie.find("span", class_="normal-price")
        if p_price_tag:
            p_price_text = p_price_tag.get_text(strip=True).replace(".", "")
            p_price = float(re.search(regex, p_price_text).group().replace(",", "."))
        else:
            p_price = c_price

        movies["vendor"].append("imusic")
        movies["title"].append(movie.find("a", title=True)["title"])
        movies["c_price"].append(c_price)
        movies["p_price"].append(p_price)
        movies["sale"].append((p_price - c_price) / p_price)


df = pd.DataFrame(movies)
df.to_csv("../data/imusic.csv", index=False)

print("Importing complete, CSV data stored")
