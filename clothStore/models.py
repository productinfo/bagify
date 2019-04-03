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
    color = models.ForeignKey('Color', related_name='images', on_delete=models.CASCADE)

    image = models.ImageField(upload_to="products_images/")
    color = models.CharField(max_length=30, blank=True, null=True)
    main_display = models.BooleanField(default=False)


class Color(models.Model):
    item = models.ForeignKey('Item', related_name='colors', on_delete=models.CASCADE)

    label = models.CharField(max_length=30)
    value = models.CharField(max_length=20)
    stock = models.IntegerField(default=0)

    sold_units = models.IntegerField(default=0)


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
    main_image = models.ImageField(upload_to="main_images/", null=True, blank=True)

    total_units_sold = models.IntegerField(default=0)
    insertion_date = models.DateTimeField(default=timezone.now)

    def getImagesWithColor(self, colorLabel):
        pass

    def __str__(self):
        return f'{self.name}'
