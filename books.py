import json


class Book:
    def __init__(self, title, author, price, publisher, cover, year, series, pages,
                 shop_url,
                 img_url):
        self.title = title
        self.author = author
        self.price = price
        self.publisher = publisher
        self.cover = cover
        self.year = year
        self.series = series
        self.pages = pages
        self.shop_url = shop_url
        self.img_url = img_url

    def __str__(self):
        return f'Title: {self.title} \n' \
               f'Author: {self.author} \n' \
               f'Price: {self.price} \n' \
               f'Publisher: {self.publisher} \n' \
               f'Cover: {self.cover} \n' \
               f'Year of publish: {self.year} \n' \
               f'Series: {self.series} \n' \
               f'Pages: {self.pages} \n' \
               f'ShopUrl: {self.shop_url} \n' \
               f'Image: {self.img_url}'

    pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
