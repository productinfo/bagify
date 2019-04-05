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

        self.blue = Color.objects.create(label='blue', value='#00F', item=self.item)
        self.black = Color.objects.create(label='Black', value='#000', item=self.item)
        self.grey = Color.objects.create(label='grey', value='#CCC', item=self.item)

        Image.objects.create(item=self.item, image=image, color=self.blue)
        Image.objects.create(item=self.item, image=image)
        Image.objects.create(item=self.item, image=image, color=self.grey)
        Image.objects.create(item=self.item, image=image, color=self.black)
        Image.objects.create(item=self.item, image=image)

    def test_basic_data(self):
        """Tests if Item contains it's images """
        self.assertEqual(self.item.images.count(), 5);
        self.assertEqual(self.item.get_images_with_color('blue').count(), 1)
        self.assertEqual(self.item.get_images_with_color('black').count(), 1)
