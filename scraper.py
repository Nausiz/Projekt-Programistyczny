from bs4 import BeautifulSoup
import requests
from whisky_bottle import Whisky
import time


def str_to_float(number: str):
    try:
        float(number)
        return float(number)
    except:
        return number


def find_item_id(script):
    item_id = script.split("',", 1)[1]
    item_id = (item_id.split(',', 1)[0]).strip().strip("'")
    return item_id


data_prefix = 'https://www.whiskybase.com/json.php?id='

# Temp - will change it when database is ready
links = ['https://shop.whiskybase.com/us/paul-john-pedro-ximenez.html',
         'https://shop.whiskybase.com/us/glenfarclas-1988.html',
         'https://shop.whiskybase.com/us/glenfiddich-12-year-old-133167006.html']


def scrap_data(links: list):
    whisky_list = []

    for link in links:
        # Find data on page
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        info_row = soup.find('div', class_='container productpage')

        name = info_row.find('h1').text
        description = info_row.find('div', class_='product-description').text

        price = info_row.find('span', class_='price highlight-txt').text
        price = price.strip('€')
        price = str_to_float(price.replace(',', '.'))

        img_url = info_row.find('div', class_='item zoom').attrs['data-src']
        brand = info_row.find('div', class_='col-xs-3 brand').find('img').attrs['src']

        avb = info_row.find('button', class_='btn-addtocart place-in-cart button').attrs['data-available']
        if avb == 'true':
            availability = "Dostępny"
        else:
            availability = "Niedostępny"

        # Create link to json dataset
        scripts = info_row.find_all('script')[1].text
        dataset_link = data_prefix + find_item_id(scripts)

        # Get data from json
        j_data = requests.get(dataset_link).json()
        rating = (j_data.get('rating'))
        alcohol = (j_data.get('strength'))
        size = j_data.get('size')
        age = j_data.get('age')
        bottled = j_data.get('bottled')

        # Create whisky object and add to list
        W = Whisky(name, description, price, rating, brand, alcohol, size, age, bottled, availability, link, img_url)
        whisky_list.append(W)

        # Mark link as visited

    return whisky_list

# Send data from list to the database - when database is ready


start_time = time.time()

whisky_list = scrap_data(links)
for whisky in whisky_list:
    print(whisky)
    print()

print("--- %s seconds ---" % (time.time() - start_time))