from django.contrib import admin
from .models import Item, Category, Image, Order, CarouselImage, Address, Color
# Register your models here.

class ImagesInline(admin.StackedInline):
    model = Image
    extra = 1

class ColorInline(admin.StackedInline):
    model = Color
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'price',
        'category',
        'gender',
        'description',
        'total_units_sold',
    ]
    inlines = [
        ColorInline,
        ImagesInline,
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(CarouselImage)
admin.site.register(Order)
admin.site.register(Address)
