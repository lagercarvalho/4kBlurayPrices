from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd
import re
from tqdm import tqdm

url = "https://cdon.se/film/4k-ultra-hd/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

home_page = requests.get(url, headers=headers)
home_soup = BeautifulSoup(home_page.text, "html.parser")
pages = int(home_soup.find_all("li", class_="pagination__page")[-1].text)
print(f'Importing {pages} pages')

movies = {
    'title': [],
    'c_price': [],
    'p_price': [],
    'sale':[]
}

enum = range(pages)
if '-v' in sys.argv:
    enum = tqdm(enum, desc="Processing pages")

for page in enum:

    index_page = requests.get(f'{url}?pageIndex={page}', headers=headers)
    page_soup = BeautifulSoup(index_page.text, "html.parser")
    page_movies = page_soup.find_all("a", class_="p-c")

    for movie in page_movies:

        price_text = movie.find("span", class_="p-c__current-price").get_text(strip=True)
        c_price = int(re.search(r'\b\d+\b', price_text).group())

        p_price_tag = movie.find("span", class_="p-c__original-price-number")
        p_price = int(re.search(r'\b\d+\b', p_price_tag.get_text(strip=True)).group()) if p_price_tag else c_price

        movies['title'].append(movie.find("span", class_="p-c__title").get_text(strip=True))
        movies['c_price'].append(c_price)
        movies['p_price'].append(p_price)
        movies['sale'].append((p_price - c_price)/ p_price)


df = pd.DataFrame(movies)
df.to_csv('data/cdon.csv', index=False)

print('Importing complete, CSV data stored')