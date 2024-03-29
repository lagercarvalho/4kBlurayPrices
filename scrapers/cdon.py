from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import re
from tqdm import tqdm
import json
import os

def scrape_cdon():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f"{script_dir}/../config.json", "r") as f:
        config = json.load(f)["cdon"]

    url = config["url"]
    headers = config["headers"]

    home_page = requests.get(url, headers=headers)
    home_soup = BeautifulSoup(home_page.text, "html.parser")
    pages = int(home_soup.find_all("li", class_="pagination__page")[-1].text)

    movies = {"vendor": [], "title": [], "c_price": [], "p_price": [], "sale": [], "status":[] , "img_src":[], "list_src":[]}

    enum = range(pages)
    if "-v" in sys.argv:
        enum = tqdm(enum, desc="Processing CDON pages")

    for page in enum:

        index_page = requests.get(f"{url}?pageIndex={page}", headers=headers)
        page_soup = BeautifulSoup(index_page.text, "html.parser")
        page_movies = page_soup.find_all("a", class_="p-c")

        for movie in page_movies:
            payload = json.loads(movie["data-payload"])
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
            filtered_title = re.sub(r'\s*\(([^)]+)\)', '', movie["title"])
            movies["title"].append(filtered_title)
            movies["list_src"].append(f'https://cdon.se{movie["href"]}')
            movies["img_src"].append(movie.find("img", class_="p-c__image")["src"])
            movies["c_price"].append(c_price)
            movies["p_price"].append(p_price)
            movies["sale"].append((p_price - c_price) / p_price)
            movies["status"].append(payload["productState"])


    df = pd.DataFrame(movies)
    df.to_csv(f"{script_dir}/../data/cdon.csv", index=False)

    if "-v" in sys.argv:
        print("Importing complete, CSV data stored")

if __name__ == "__main__":
    scrape_cdon()