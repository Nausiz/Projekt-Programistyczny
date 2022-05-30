from crawler import Crawler
from scraper import Scraper


if __name__ == '__main__':
    Crawler(urls=['https://www.taniaksiazka.pl/']).run()
    Scraper(query='SELECT url FROM ksiazki WHERE scrapped = False').scrap_data()
