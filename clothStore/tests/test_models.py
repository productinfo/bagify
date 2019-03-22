from django.test import TestCase
from clothStore.models import *

class ItemPropertiesTestCase(TestCase):
    def setUp(self):
        Item.objects.create(name='cortez', description='fast shoe', price=39.99)
        Item.objects.create(name='whoosh', description='the sound you make while running', price=29.99)
        Item.objects.create(name='pink pijamas', description='cozy', price=19.99)

    def test_basic_data(self):
        """ Items exist and have the default properties """
        pijama = Item.objects.get(name='pink pijamas')
        cortez = Item.objects.get(name='cortez')

        self.assertEqual(float(pijama.price), 19.99)
        self.assertEqual(pijama.description, 'cozy')
        self.assertEqual(cortez.sizes, None)
        self.assertEqual(cortez.colors, None)

    def test_improper_usage_of_color_methods(self):
        """ Using color methods improperly will return an int and not an error """

        pijama = Item.objects.get(name='pink pijamas')
        cortez = Item.objects.get(name='cortez')

        self.assertEqual(pijama.rmColors(), 1)
        self.assertEqual(pijama.rmColors('blue', 'green', 'mario'), 1)
        self.assertEqual(pijama.rmColors(13), 1)
        self.assertEqual(cortez.getColors(), None)

        cortez.addColors(1, 5, 'green', ['blue', 'pink'], 'luigi')
        self.assertEqual(cortez.getColors(), ['green', 'luigi'])

    def test_usage_colors(self):
        """ Tests if color methods are doing what they should """
        cortez = Item.objects.get(name='cortez')
        cortez.addColors('blue', 'green', 'brown')

        self.assertEqual(cortez.getColors(), ['blue', 'green', 'brown'])

        cortez.rmColors('blue', 'orange', 'brown')

        self.assertEqual(cortez.getColors(), ['green'])

        cortez.addColors('red', ['tango'])
        cortez.rmColors(12, 'green')

        self.assertEqual(cortez.getColors(), ['red'])

    def test_usage_sizes_and_stocks(self):
        """ Tests if Size and Stock methods work properly """
        cortez = Item.objects.get(name='cortez')
        whoosh = Item.objects.get(name='whoosh')

        self.assertEqual(cortez.getSizes(), None)

        cortez.addSize('Medium', 10)
        cortez.addSize('Large')
        self.assertEqual(cortez.getSizes(), [{'size': 'medium', 'stock': 10 }, {'size': 'large', 'stock': 0}])

        cortez.rmSize('large')
        self.assertEqual(cortez.getSizes(), [{'size': 'medium', 'stock': 10}])

        whoosh.addSize('Small', 50)
        self.assertEqual(whoosh.changeStock('small', 100), 0)

        self.assertEqual(whoosh.getStock('small'), 150)

        whoosh.changeStock('SMALL', 1000, 'set')
        self.assertEqual(whoosh.getStock('Small'), 1000)

    def test_improper_usage_of_size_stock_methods(self):
        """Checks if Size and Stock methods responds as they should to improper calls """

        cortez = Item.objects.get(name='cortez')

        self.assertEqual(cortez.addSize(['medium', 4]), 1)

        self.assertEqual(cortez.rmSize('12'), 1)

        cortez.addSize('Medium', 15)
        self.assertEqual(cortez.changeStock('medium', 50, 'change'), 3)
        self.assertEqual(cortez.getStock('large'), None)


#
# class CategoryTestCase
#
# class OrderTestCase

class ItemRelationships(TestCase):
    def setUp(self):
        Item.objects.create(name='Phoenix', price=99.99)
        Category.objects.create(name='Mythical Creatures')

        Image.objects.create()
        Image.objects.create()
        Image.objects.create()
