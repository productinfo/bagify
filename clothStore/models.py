from django.db import models
import json

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    colors = models.TextField(blank=True, null=True)
    sizes = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def addColors(self, *args):
        current = json.loads(self.colors)
        for color in args:
            if isinstance(color, str) and color not in current:
                current.append(color)
        self.colors = json.dumps(current)

    def rmColors(self, *args):
        if args:
            if args[0] == 'all':
                self.colors = ''
            else:
                current = json.loads(self.colors)
                for color in args:
                    if isinstance(color, str) and color in current:
                        current = [x for x in current if x != color]

                self.colors = json.dumps(current)

    def getColors(self, property):
        current = json.loads(self.colors)
        return [color for color in self.colors]

    def getSizes(self):
        current = json.loads(self.sizes)
        return [size for size in self.sizes]



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
