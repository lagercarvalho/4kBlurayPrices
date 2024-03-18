import pandas as pd
import requests
import sys
import math
from tqdm import tqdm
import json

def scrape_kvarn():

    with open("../config.json", "r") as f:
        config = json.load(f)["kvarn"]

    url = config["url"]

    page = requests.post(url, json=config["json"])
    total_movies = page.json()["result"]

    movies = {"vendor": [], "title": [], "c_price": [], "p_price": [], "sale": [], "img_src":[], "list_src":[]}

    rounds = math.ceil(total_movies / 100)

    enum = range(1, rounds + 1)
    if "-v" in sys.argv:
        print(f"Importing {total_movies} movies")
        enum = tqdm(enum, desc="Processing pages")

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
            movies["title"].append(movie["name"]["sv"])
            movies["c_price"].append(curr_price)
            movies["p_price"].append(prev_price)
            movies["sale"].append((prev_price - curr_price) / prev_price)

    df = pd.DataFrame(movies)
    df.to_csv("../data/kvarn.csv", index=False)

    if "-v" in sys.argv:
        print("Importing complete, CSV data stored")

if __name__ == "__main__":
    scrape_kvarn()