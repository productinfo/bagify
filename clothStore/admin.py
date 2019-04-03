from django.contrib import admin
from .models import Item, Category, Image, Order, CarouselImage, Address
# Register your models here.

class ImagesInline(admin.StackedInline):
    model = Image
    extra = 3

class ItemAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'price',
        'category',
        'gender',
        'description',
        'sold_units',
        'main_image'
    ]
    inlines = [
        ImagesInline
    ]



admin.site.register(Item, ItemAdmin)
admin.site.register(Category)

admin.site.register(CarouselImage)

admin.site.register(Order)
admin.site.register(Address)
