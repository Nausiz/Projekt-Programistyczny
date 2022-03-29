class Whisky:
    def __init__(self, name, desc, price, rating, brand, alcohol, size, age, bottled, availability, shop_url, img_url):
        self.name = name
        self.desc = desc
        self.price = price
        self.rating = rating
        self.brand = brand
        self.alcohol = alcohol
        self.size = size
        self.age = age
        self.bottled = bottled
        self.availability = availability
        self.shop_url = shop_url
        self.img_url = img_url

    def __str__(self):
        return f'Name: {self.name} \n' \
               f'Description: {self.desc} \n' \
               f'Price: {self.price} \n' \
               f'Rating: {self.rating} \n' \
               f'Brand: {self.brand} \n' \
               f'Alcohol: {self.alcohol} \n' \
               f'Size: {self.size} \n' \
               f'Age: {self.age} \n' \
               f'Bottled: {self.bottled} \n' \
               f'Availability: {self.availability} \n' \
               f'ShopUrl: {self.shop_url} \n' \
               f'Image: {self.img_url}'
    pass

