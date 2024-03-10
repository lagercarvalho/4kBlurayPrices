from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import re
from tqdm import tqdm
import json

with open("../config.json", "r") as f:
    config = json.load(f)["cdon"]

url = config["url"]
headers = config["headers"]

home_page = requests.get(url, headers=headers)
home_soup = BeautifulSoup(home_page.text, "html.parser")
pages = int(home_soup.find_all("li", class_="pagination__page")[-1].text)
print(f"Importing {pages} pages")

movies = {"vendor": [], "title": [], "c_price": [], "p_price": [], "sale": []}

enum = range(pages)
if "-v" in sys.argv:
    enum = tqdm(enum, desc="Processing pages")

for page in enum:

    index_page = requests.get(f"{url}?pageIndex={page}", headers=headers)
    page_soup = BeautifulSoup(index_page.text, "html.parser")
    page_movies = page_soup.find_all("a", class_="p-c")

    for movie in page_movies:
        regex = r"\d+(?:,\d+)?"
        price_text = (
            movie.find("span", class_="p-c__current-price")
            .get_text(strip=True)
            .replace("\xa0", "")
        )
        c_price = float(re.search(regex, price_text).group().replace(",", "."))

        p_price_tag = movie.find("span", class_="p-c__original-price-number")
        if p_price_tag:
            p_price_text = p_price_tag.get_text(strip=True).replace("\xa0", "")
            p_price = float(re.search(regex, p_price_text).group().replace(",", "."))
        else:
            p_price = c_price

        movies["vendor"].append("cdon")
        movies["title"].append(
            movie.find("span", class_="p-c__title").get_text(strip=True)
        )
        movies["c_price"].append(c_price)
        movies["p_price"].append(p_price)
        movies["sale"].append((p_price - c_price) / p_price)


df = pd.DataFrame(movies)
df.to_csv("../data/cdon.csv", index=False)

print("Importing complete, CSV data stored")
