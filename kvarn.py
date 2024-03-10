import pandas as pd
import requests
import sys
import math
from tqdm import tqdm

url = "https://www.kvarnvideo.se/backend/jsonrpc/v1?webshop=4862"
count_json = {
    "id":12,
    "jsonrpc":"2.0",
    "method":"Article.count",
    "params":[{"/showInArticlegroups":{
        "containsAny":[8646737,8646739,8646743,8646779,8646877,8646745,8646789,8646747,8646775,8646749,8646751,8646803,8646753,8646755,8646757,8646759,8646761,8646801,8646763,8646777,8646765]
    }}]
}

page = requests.post(url, json=count_json)
total_movies = page.json()['result']
print(f'Importing {total_movies} movies')

movies = {
    'vendor': [],
    'title': [],
    'c_price': [],
    'p_price': [],
    'sale':[]
}

rounds = math.ceil(total_movies / 100)

enum = range(1, rounds + 1)
if '-v' in sys.argv:
    enum = tqdm(enum, desc="Processing pages")

for x in enum:
    body = {
    "id": 11,
    "jsonrpc":"2.0",
    "method":"Article.list",
    "params":[{"isBuyable":True,"name":"sv","pricing":True,"showPricesIncludingVat":True},
        {"filters":{"/showInArticlegroups":
            {"containsAny":[8646739,8646743,8646779,8646877,8646745,8646789,8646747,8646775,8646749,8646751,8646803,8646753,8646755,8646757,8646759,8646761,8646801,8646763,8646777,8646765]}},
        "descending":True,"sort":"numSold", "limit": 99, "offset":(x-1)*100}]
    }

    page = requests.post(url, json=body)
    data = page.json()

    for movie in data['result']:
        pricing_info = movie['pricing'][0]
        prev_price = pricing_info['regular']['incVat']['SEK']
        curr_price = pricing_info['specialOffer']['incVat']['SEK'] if 'specialOffer' in pricing_info else prev_price

        movies['vendor'].append('kvarn')
        movies['title'].append(movie['name']['sv'])
        movies['c_price'].append(curr_price)
        movies['p_price'].append(prev_price)
        movies['sale'].append((prev_price - curr_price) / prev_price)

df = pd.DataFrame(movies)
df.to_csv('data/kvarn.csv', index=False)

print('Importing complete, CSV data stored')