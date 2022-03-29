from bs4 import BeautifulSoup
import requests
import json
from whisky_bottle import Whisky


def str_to_float(number: str):
    try:
        float(number)
        return float(number)
    except:
        return number


# Temp - will change it when database is ready
links = ['https://shop.whiskybase.com/us/paul-john-pedro-ximenez.html',
         'https://shop.whiskybase.com/us/glenfarclas-1988.html']

def scrap_data(links: list):
    whisky_list = []

    for link in links:
        # Find data on page
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        info_row = soup.find('div', class_='container productpage')
        price = info_row.find('span', class_='price highlight-txt').text
        price = price.strip('€')
        price = str_to_float(price.replace(',', '.'))
        name = info_row.find('h1').text
        description = info_row.find('div', class_='product-description').text
        img_url = info_row.find('div', class_='item zoom').attrs['data-src']
        brand = info_row.find('div', class_='col-xs-3 brand').find('img').attrs['src']

        # Find data in script - maybe coming soon
        # script = info_row.find_all('script')

        # Create whisky object and add to list
        W = Whisky(name, description, price, brand, 0, 0, 0, 0, 0, link, img_url)
        whisky_list.append(W)

        # Mark link as visited

    for whisky in whisky_list:
        print(whisky)
        print()

    return whisky_list

# Send data from list to the database - when database is ready