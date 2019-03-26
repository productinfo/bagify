from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

import json
# Create your models here.

class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel_images/")
    item = models.ForeignKey('Item', related_name='carousel', on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=800, null=True, blank=True)

class Image(models.Model):
    item = models.ForeignKey('Item', related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products_images/")
    color = models.CharField(max_length=30, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=50)

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    items = models.TextField()
    address = models.TextField()
    total = models.DecimalField(decimal_places=2, max_digits=9)

class Item(models.Model):
    GENDER_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex')
    )

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)

    category = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    colors = models.TextField(blank=True, null=True)
    sizes = models.TextField(blank=True, null=True)
    stock = models.TextField(blank=True, null=True)
    main_image = models.ImageField(upload_to="main_images/", null=True, blank=True)
    sold_units = models.IntegerField(default=0)
    insertion_date = models.DateTimeField(default=timezone.now)

    def addColors(self, *args):
        if self.colors:
            current = json.loads(self.colors)
        else:
            current = []

        if not args:
            return 1

        for color in args:
            if isinstance(color, str) and color not in current:
                current.append(color.lower())
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

    def getSizes(self):
        if not self.sizes:
            return None
        return json.loads(self.sizes)

    def addSizes(self, *args):
        if not args:
            return 1

        if self.sizes:
            current = json.loads(self.sizes)
        else:
            current = []

        for size in args:
            if isinstance(size, str) and size.lower() not in current:
                current.append(size.lower())

        self.sizes = json.dumps(current)
        return 0

    def rmSizes(self, *args):
        if not self.sizes or not args:
            return 1
        sizes = json.loads(self.sizes)
        for size in args:
            sizes = [x for x in sizes if x != size.lower()]
        self.sizes = json.dumps(sizes)
        return 0

    def changeStock(self, stock=0, size='', color='', action = 'set'):
        if action != 'add' and action != 'set':
            return 3

        if type(stock) != int or stock < 1 or type(size) != str or type(color) != str:
            return 1

        if self.stock:
            stocks = json.loads(self.stock)
        else:
            stocks = []

        for i in range(len(stocks)):
            if stocks[i]['size'] == size.lower() and stocks[i]['color'] == color.lower():
                if action == 'add':
                    stocks[i]['stock'] = stocks[i]['stock'] + stock
                elif action == 'set':
                    stocks[i]['stock'] = stock
                break;
        else:
            stocks.append({ 'size': size.lower(), 'color': color.lower(), 'stock': stock })

        self.stock = json.dumps(stocks)
        return 0

    def getStock(self, size = '', color = ''):
        if not self.stock:
            return 1

        stock = json.loads(self['stock'])

        if not size and not color:
            return stock
        else:
            return next(item for item in stock if item['color'] == color and item['size'] == size)
        return 2

    def getStocks(self):
            if not self.stock:
                return None
            return json.loads(self.stock)

    def getImagesWithColor(self, color):
        images = self.images.filter(color=color)
        return images;

    def __str__(self):
        return f'{self.name}'
