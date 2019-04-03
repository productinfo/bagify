from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
# Create your models here.

class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel_images/")
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=300, null=True, blank=True)
    item = models.ForeignKey('Item', related_name='carousel', on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=800, null=True, blank=True)

class Image(models.Model):
    item = models.ForeignKey('Item', related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products_images/")
    color = models.CharField(max_length=30, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="categories_images/")

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    items = models.TextField()
    address = models.TextField()
    total = models.DecimalField(decimal_places=2, max_digits=9)

class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    default = models.BooleanField(default=False)
    state = models.CharField(blank=True, max_length=100)
    address = models.CharField(blank=True, max_length=100)
    complement = models.CharField(blank=True, max_length=100)
    zip = models.CharField(blank=True, max_length=100)

    @staticmethod
    def get_default(self, user):
        print(self)
        address = user.addresses.filter(default=True)[0]
        return address

class Item(models.Model):
    GENDER_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex')
    )

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    colors = models.TextField(default='[]', null=True)
    stock = models.TextField(default='[]')
    main_image = models.ImageField(upload_to="main_images/", null=True, blank=True)

    sold_units = models.IntegerField(default=0)
    insertion_date = models.DateTimeField(default=timezone.now)

    def addColor(self, color):
        if self.colors:
            current = json.loads(self.colors)
        else:
            current = []

        if not args:
            return 1

        for color in args:
            if isinstance(color, dict):
                color.label = color.label.lower()
                current.append(color)
        self.colors = json.dumps(current)

    def rmColors(self, *args):
        if not self.colors or not args:
            return 1

        if args[0] == 'all':
            self.colors = ''
            return 0
        else:
            current = json.loads(self.colors)
            for color in args:
                if isinstance(color, str) and color.lower() in current:
                    current = [x for x in current if x != color.lower()]

            self.colors = json.dumps(current)
        return 0

    def getColors(self):
        if not self.colors:
            return None
        return json.loads(self.colors)

    def changeStock(self, action, stock=0, color=''):
        if action != 'add' and action != 'set':
            return 3

        if type(stock) != int or stock < 1 or type(color) != str:
            return 1

        if self.stock:
            stocks = json.loads(self.stock)
        else:
            stocks = []

        for i in range(len(stocks)):
            if stocks[i]['color'] == color.lower():
                if action == 'add':
                    stocks[i]['stock'] = stocks[i]['stock'] + stock
                elif action == 'set':
                    stocks[i]['stock'] = stock
                break;
        else:
            stocks.append({'color': color.lower(), 'stock': stock })

        self.stock = json.dumps(stocks)
        return 0

    def getStock(self, color = ''):
        if not self.stock:
            return 1

        stock = json.loads(self['stock'])

        if not color:
            return stock
        else:
            return next(item for item in stock if item['color'] == color)
        return 2

    def getStocks(self):
            if not self.stock:
                return None
            return json.loads(self.stock)

    def getImagesWithColor(self, colorLabel):
        images = self.images.filter(color=colorLabel)
        return images;

    def __str__(self):
        return f'{self.name}'
