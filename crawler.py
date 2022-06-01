import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from connect import select, insert, update

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:
    def __init__(self, urls=[]):
        l1 = select('select url from crawler where visited = True')
        l2 = select('select url from crawler where visited = False')
        self.visited_urls = [x[0] for x in l1]
        self.urls_to_visit = urls + [x[0] for x in l2]

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            if url != None and 'https://www.taniaksiazka.pl' in url:
                insert(url)
                if url != None and "-p-" in url:
                    insert(url, 'ksiazki')
                self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)
                update(url)


if __name__ == '__main__':
    # Crawler(urls=['https://www.whiskybase.com/market/browse/']).run()
    # Crawler(urls=['https://www.empik.com/']).run()
    Crawler(urls=['https://www.taniaksiazka.pl/']).run()
