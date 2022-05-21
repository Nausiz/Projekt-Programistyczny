import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from books import Book
from connect import select, insert_book, update_meta, update_timestamp, update_book

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Scraper:

    def __init__(self, query):
        self.urls_to_scrap = select(query)

    def check_urls(self):
        print(self.urls_to_scrap)

    def str_to_float(self, number: str):
        try:
            float(number)
            return float(number)
        except:
            return number

    def update_book_data(self, book, link):
        check = select("""SELECT * FROM k_data WHERE shop_url = '""" + book.shop_url + """'""")
        if len(check) > 0:
            print("Exist, updating")
            update_book(link, book)
        else:
            insert_book(book)

    def scrap_data(self):
        books_list = []

        for url in self.urls_to_scrap:
            try:
                # Clean url
                link = re.sub("[()'',]", '', str(url))

                if re.search("games-p", link) is not None or re.search("audiobook", link) is not None:
                    continue

                # Set default values
                title = author = publisher = cover = series = img_url = '-'
                price = year = pages = -1
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
                price = '.'.join([price_zl, price_gr])
                img_url = img_tab.find('img').attrs['src']

                for x in meta:
                    if x.text.startswith("Autor:") or x.text.startswith("Autorzy:"):
                        author = x.text.split(': ', 1)[1]
                        # print(author)
                    elif x.text.startswith("Wydawnictwo") or x.text.startswith("Producent"):
                        publisher = x.text.split(' ', 1)[1]
                        # print(publisher)
                    elif x.text.startswith("Oprawa"):
                        cover = x.text.split(': ', 1)[1]
                        # print(cover)
                    elif x.text.startswith("Ilość stron"):
                        pages = int(x.text.split(': ', 1)[1])
                        # print(pages)
                    elif x.text.startswith("Seria"):
                        series = x.text.split(' ', 1)[1]
                        # print(series)
                    elif x.text.startswith("Rok wydania:"):
                        year = x.text.split(': ', 1)[1]
                        # print(year)
                    else:
                        continue

                if author == '-':
                    continue

                # Create book object and add to list
                b = Book(title, author, price, publisher, cover, year, series, pages,
                         shop_url,
                         img_url)
                books_list.append(b)

                # Mark link as visited and add timestamp
                dt = datetime.now()
                update_timestamp(link, dt)
                q_status = """ UPDATE ksiazki SET scrapped = True WHERE url = '""" + link + """'"""
                update_meta(q_status)

                self.update_book_data(b, link)

            except Exception:
                logging.exception(f'Failed to scrap: {url}')


if __name__ == '__main__':
    Scraper(query='SELECT url FROM ksiazki WHERE scrapped = False').scrap_data()
