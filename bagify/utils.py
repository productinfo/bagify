import json

from django.conf import settings
from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm

from .models import *

def makeOrder():
	pass

def indexCache(request):
	cache_key = 'indexPageData'
	cache_time = 21600
	data = cache.get(cache_key)

	if not data:
		 data.carousel = CarouselImage.objects.all()
		 data.mostPopular = Item.objects.order_by('-sold_units')[:8]
		 data.newestAdditions = Item.objects.order_by('-id')[:8]

	cache.set(cache_key, data, cache_time)

	return JsonResponse(data, safe=False)

# gets the cart stored in the cookies
def getCart(request):
	cookies = request.COOKIES.get('cart')
	if not cookies:
		return []

	cart = json.loads(cookies)
	bigCart = []  # new cart which will contain all data being passed back

	for product in cart:
		item = {
			'id': product['id'],
			'color': product['color']
		}
		productModel = Item.objects.filter(pk=product['id'])[0]
		if not productModel:
			continue

		if productModel.category:
			item['category'] = productModel.category.name

		item['price'] = float(productModel.price)
		item['name'] = productModel.name
		item['image'] = productModel.colors.get(label__iexact=product['color']).get_main_image().image.url

		bigCart.append(item)

	return bigCart

def give_me_money_paypal(request, price, name, unique_id):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": price,
        "item_name": name,
        "invoice": unique_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    return form
