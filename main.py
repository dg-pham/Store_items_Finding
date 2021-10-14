import re

import requests
from bs4 import BeautifulSoup

search_term = input('What product do you want to search for? ')

# get HTML doc from url (&N=4131 = in stock)
url = f'https://www.newegg.com/p/pl?d={search_term}&N=4131'
page = requests.get(url).text
doc = BeautifulSoup(page, 'html.parser')

# get number of pages
page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split('/')[-2].split('>')[-1][:-1])
# print(pages)

# tuple
items_found = {}

for page in range(1, pages + 1):
    # get HTML doc each page
    url = f'https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}'
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    # get all items
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_term))

    # get items links and prices
    for item in items:
        # get links
        parent = item.parent
        if parent.name != 'a':
            continue

        # links
        link = parent['href']

        # get prices
        next_parent = item.find_parent(class_="item-container")
        try:
            # prices
            price = next_parent.find(class_="price-current").find('strong').string
            items_found[item] = {'price': int(price.replace(',', '')), 'link': link}
        finally:
            pass

# soft
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

# print items names, prices, links
for item in sorted_items:
    print(item[0])
    print(f'${item[1]["price"]}')
    print(item[1]['link'])
    print('-------------------------------')
