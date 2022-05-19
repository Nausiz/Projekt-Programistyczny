from bs4 import BeautifulSoup
import requests
from books import Book
import time
import json


def str_to_float(number: str):
    try:
        float(number)
        return float(number)
    except:
        return number

# Temp - will change it when database is ready
links = ['https://www.taniaksiazka.pl/panna-goloborze-tom-1-aleksandra-seliga-p-1640642.html',
         'https://www.taniaksiazka.pl/cztery-muzy-sophie-haydock-p-1664460.html',
         'https://www.taniaksiazka.pl/ksiega-pieciu-kregow-miyamoto-musashi-p-232524.html',
         'https://www.taniaksiazka.pl/te-wiedzmy-nie-plona-isabel-sterling-p-1350645.html',
         'https://www.taniaksiazka.pl/the-art-of-business-wars-david-brown-p-1532993.html']


def scrap_data(links: list):
    books_list = []

    for link in links:
        # Default values
        title = author = price = rating = publisher = cover = year = series = pages = img_url = '-'
        shop_url = link

        # Find data on page
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        content = soup.find('div', class_='col-left4')
        info = soup.find('div', id='DetailsModule')
        meta = info.find_all('li')
        img_tab = content.find('li', 'image0 active')
        price_tab = content.find('div', class_='radio-line')
        price_zl = price_tab.find_all('span')[1].text
        price_gr = price_tab.find('strong').text
        price_gr = price_gr.split(',', 1)[1]
        price_gr = price_gr.split(' ', 1)[0]

        # Find book details
        title = content.find('h1').text.strip()
        price = str_to_float('.'.join([price_zl,price_gr]))
        img_url = img_tab.find('img').attrs['src']
        for x in meta:
            if x.text.startswith("Autor:"):
                author = x.text.split(': ', 1)[1]
                #print(author)
            elif x.text.startswith("Wydawnictwo") or x.text.startswith("Producent"):
                publisher = x.text.split(' ', 1)[1]
                #print(publisher)
            elif x.text.startswith("Oprawa"):
                cover = x.text.split(': ', 1)[1]
                #print(cover)
            elif x.text.startswith("Ilość stron"):
                pages = int(x.text.split(': ', 1)[1])
                #print(pages)
            elif x.text.startswith("Seria"):
                series = x.text.split(' ', 1)[1]
                #print(series)
            elif x.text.startswith("Rok wydania:"):
                year = x.text.split(': ', 1)[1]
                #print(year)
            else:
                continue
        #print(meta)

        # Create book object and add to list
        B = Book(title, author, price, rating, publisher, cover,  year, series, pages,
                 shop_url,
                 img_url)
        books_list.append(B)

        # Mark link as visited

    return books_list

# Send data from list to the database - when database is ready


start_time = time.time()

books = scrap_data(links)

json_books = []
for b in books:
    x = b.to_json()
    json_books.append(x)

for x in json_books:
    print(x)

print("--- %s seconds ---" % (time.time() - start_time))