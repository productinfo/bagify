from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from django_countries.fields import CountryField

import json
# Create your models here.

class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel_images/")
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=300, null=True, blank=True)

    item = models.ForeignKey('Item', related_name='carousel_item', on_delete=models.SET_NULL, null=True, blank=True)

    main = models.BooleanField(default=True)
    url = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    item = models.ForeignKey('Item', related_name="images", on_delete=models.CASCADE)
    color = models.ForeignKey('Color', related_name='images', on_delete=models.CASCADE, null=True)

    image = models.ImageField(upload_to="products_images/")
    main_display = models.BooleanField(default=False)

    def __str__(self):
        return f'Image of {self.item} with {self.color} color'

class Color(models.Model):
    item = models.ForeignKey('Item', related_name='colors', on_delete=models.CASCADE)

    label = models.CharField(max_length=30)
    value = models.CharField(max_length=20)
    stock = models.IntegerField(default=0)

    sold_units = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.label} color for {self.item}'

    def get_main_image(self):
        query = Image.objects.filter(color=self, main_display=True)[0]
        return query or None


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="categories_images/")

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)

    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)

    items = models.TextField()

    address = models.TextField()
    total = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return f'Order n.{self.pk} - {self.date.strftime("%d/%m/%y")}'


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField()
    address = models.CharField(max_length=100)
    complement = models.CharField(blank=True, null=True, max_length=100)
    zip = models.CharField(max_length=100)

    @staticmethod
    def get_default(self, user):
        address = user.addresses.filter(default=True)[0]
        return address

    def __str__(self):
        return f'Address of {self.user}'

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

    total_units_sold = models.IntegerField(default=0)
    insertion_date = models.DateTimeField(default=timezone.now)

    def get_images_with_color(self, colorLabel):
        query = self.colors.filter(label__iexact=colorLabel)[0]
        return query.images or None

    def get_display_images(self):
        query = Image.objects.filter(item=self, main_display=True)
        return query or None

    def __str__(self):
        return f'{self.name}'
