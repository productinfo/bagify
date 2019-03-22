from django.db import models
import json

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    colors = models.TextField(blank=True, null=True)
    sizes = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def addColors(self, *args):
        if self.colors:
            current = json.loads(self.colors)
        else:
            current = []

        for color in args:
            if isinstance(color, str) and color not in current:
                current.append(color.lower())
        self.colors = json.dumps(current)

    def rmColors(self, *args):
        if not self.colors or not args:
            return 1

        if args:
            if args[0] == 'all':
                self.colors = ''
                return 0
            else:
                current = json.loads(self.colors)
                for color in args:
                    if isinstance(color, str) and color in current:
                        current = [x for x in current if x != color]

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

    def addSize(self, sizeName, stock = 0):
        if type(sizeName) != str:
            return 1

        if self.sizes:
            current = json.loads(self.sizes)
        else:
            current = []

        current.append({ 'size': sizeName.lower(), 'stock': stock })
        self.sizes = json.dumps(current)

        return 0

    def rmSize(self, sizeName):
        if not self.sizes:
            return 1
        sizes = json.loads(self.sizes)
        newSizes = [size for size in sizes if size['size'] != sizeName]
        self.sizes = json.dumps(newSizes)

    def changeStock(self, sizeName, number, action = 'add'):
        if action != 'add' and action != 'set':
            return 3

        if type(number) != int or number < 1 or not self.sizes:
            return 1

        sizes = json.loads(self.sizes)

        for i in range(len(sizes)):
            if sizes[i]['size'] == sizeName.lower():
                if action == 'add':
                    sizes[i]['stock'] = sizes[i]['stock'] + number
                elif action == 'set':
                    sizes[i]['stock'] = number

                self.sizes = json.dumps(sizes)
                return 0
        return 2

    def getStock(self, sizeName):
        if not self.sizes:
            return 1

        sizes = json.loads(self.sizes)
        for size in sizes:
            if size['size'] == sizeName.lower():
                return size['stock']
        return None

    def getImagesWithColor(self, color):
        images = self.images.filter(color=color)
        return images;

    def __str__(self):
        return f'{self.name}'



class Image(models.Model):
    item = models.ForeignKey(Item, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField()
    color = models.CharField(max_length=30, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=50)

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    items = models.TextField()
    address = models.TextField()
    total = models.DecimalField(decimal_places=2, max_digits=9)
