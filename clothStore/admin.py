from django.contrib import admin
from .models import Item, Category, Image, Order, CarouselImage, Address
# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(CarouselImage)
admin.site.register(Order)
admin.site.register(Address)
