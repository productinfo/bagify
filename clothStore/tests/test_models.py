from django.test import TestCase
from clothStore.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

class ItemMethodsTestCase(TestCase):
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

    def test_improper_usage_get_add_rm_methods(self):
        """ Using methods improperly will return an int and not an error """

        pijama = Item.objects.get(name='pink pijamas')
        cortez = Item.objects.get(name='cortez')

        self.assertEqual(pijama.rmColors('tango'), 1)
        self.assertEqual(pijama.rmSizes('colors', 'blue', 'green', 'mario'), 1)

        self.assertEqual(pijama.rmColors(13), 1)
        self.assertEqual(cortez.getColors(), None)

        cortez.addColors( 1, 5, 'green', ['blue', 'pink'], 'luigi')
        self.assertEqual(cortez.getColors(), ['green', 'luigi'])

        cortez.addSizes(23, 32, 49, '15', '30', 'medium', 'large')
        self.assertEqual(cortez.getSizes(), ['15', '30', 'medium', 'large'])


    def test_usage_colors(self):
        """ Tests if color methods are doing what they should """
        cortez = Item.objects.get(name='cortez')

        cortez.addColors('Blue', 'Green', 'brown')
        self.assertEqual(cortez.getColors(), ['blue', 'green', 'brown'])

        cortez.rmColors('blue', 'orange', 'brown')

        self.assertEqual(cortez.getColors(), ['green'])

        cortez.addColors('colors', 'red', ['tango'])
        cortez.rmColors('colors', 12, 'green')

        self.assertEqual(cortez.getColors(), ['red'])

    def test_usage_sizes(self):
        """ Tests if Size methods work properly """
        cortez = Item.objects.get(name='cortez')
        whoosh = Item.objects.get(name='whoosh')

        self.assertEqual(cortez.getSizes(), None)

        cortez.addSizes('Medium', 10)
        cortez.addSizes('Large')
        self.assertEqual(cortez.getSizes(), [ 'medium', 'large'])

        cortez.rmSizes('large')
        self.assertEqual(cortez.getSizes(), ['medium'])

        whoosh.addSizes('Small', 'larGe')
        self.assertEqual(whoosh.getSizes(), ['small', 'large'])

        cortez = Item.objects.get(name='cortez')

        self.assertEqual(cortez.addSizes(['medium', 4]), 0)

        self.assertEqual(cortez.rmSizes('12'), 0)

    def test_usage_of_stock_methods(self):
        """Checks if Stock methods work properly """
        cortez = Item.objects.get(name='cortez')

        cortez.changeStock(size='Medium', color='grey', stock=50)
        cortez.changeStock(size='medium', color='Grey', stock=10)

        cortez.changeStock(size='Large', color='blue', stock=100)
        cortez.changeStock(size='large', color='blue', stock= 100, action= 'add')

        self.assertEqual(cortez.getStocks(), [
        {'size':'medium', 'color':'grey', 'stock':10},
        {'size':'large', 'color':'blue', 'stock':200}])

class CarouselImageTestCase(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

        self.item = Item.objects.create(name='Cortez', price=29.99, gender='U')
        self.carouselImage = CarouselImage.objects.create(image=uploaded, item=self.item)

    def test_basic_data(self):
        self.assertEqual(self.carouselImage.item, self.item)
        self.assertEqual(CarouselImage.objects.count(), 1)

class ImageTestCase(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

        self.item = Item.objects.create(name='Swiss', price=45.00, gender='F')

        Image.objects.create(item=self.item, image=image, color='blue')
        Image.objects.create(item=self.item, image=image, color='blue')
        self.grey = Image.objects.create(item=self.item, image=image, color='grey')
        self.purble = Image.objects.create(item=self.item, image=image, color='purple')
        Image.objects.create(item=self.item, image=image)

    def test_basic_data(self):
        """Tests if Item contains it's images """
        self.assertEqual(self.item.images.count(), 5);
        self.assertEqual(self.item.getImagesWithColor('blue').count(), 2)
        self.assertEqual(self.item.getImagesWithColor('grey').count(), 1)
