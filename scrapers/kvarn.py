import pandas as pd
import requests
import sys
import math
from tqdm import tqdm
import json
import os
import re

def scrape_kvarn():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f"{script_dir}/../config.json", "r") as f:
        config = json.load(f)["kvarn"]

    url = config["url"]

    page = requests.post(url, json=config["json"])
    total_movies = page.json()["result"]

    movies = {"vendor": [], "title": [], "c_price": [], "p_price": [], "sale": [], "status": [], "img_src":[], "list_src":[]}

    rounds = math.ceil(total_movies / 100)

    enum = range(1, rounds + 1)
    if "-v" in sys.argv:
        print(f"Importing {total_movies} movies")
        enum = tqdm(enum, desc="Processing Kvarn pages")

    for x in enum:
        body = {
            "id": 11,
            "jsonrpc": "2.0",
            "method": "Article.list",
            "params": [
                {
                    "isBuyable": True,
                    "name": "sv",
                    "pricing": True,
                    "showPricesIncludingVat": True,
                    "images":True,
                    "url":"sv",
                },
                {
                    "filters": config["json"]["params"][0],
                    "descending": True,
                    "sort": "numSold",
                    "limit": 99,
                    "offset": (x - 1) * 100,
                },
            ],
        }

        page = requests.post(url, json=body)
        data = page.json()

        for movie in data["result"]:
            pricing_info = movie["pricing"][0]
            prev_price = pricing_info["regular"]["incVat"]["SEK"]
            curr_price = (
                pricing_info["specialOffer"]["incVat"]["SEK"]
                if "specialOffer" in pricing_info
                else prev_price
            )

            movies["img_src"].append(movie["images"][0])
            movies["list_src"].append(movie["url"]["sv"])
            movies["vendor"].append("kvarn")
            filtered_title = re.sub(r'\s*\(([^)]+)\)', '', movie["name"]["sv"])
            movies["title"].append(filtered_title)
            movies["c_price"].append(curr_price)
            movies["p_price"].append(prev_price)
            movies["sale"].append((prev_price - curr_price) / prev_price)
            movies["status"].append(None)

    df = pd.DataFrame(movies)
    df.to_csv(f"{script_dir}/../data/kvarn.csv", index=False)

    if "-v" in sys.argv:
        print("Importing complete, CSV data stored")

if __name__ == "__main__":
    scrape_kvarn()