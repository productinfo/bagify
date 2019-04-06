from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.conf import settings

from .models import *
from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.


#Home page
def home(request):
	carousel = CarouselImage.objects.all()
	mostPopular = Color.objects.order_by('-sold_units')[:10]
	newestAdditions = Color.objects.order_by('-id')[:10]
	categories = Category.objects.all()

	return render(request, 'bagify/index.html', {'carousel': carousel, 'newest': newestAdditions, 'popular': mostPopular, 'categories': categories })


#Account Page
def account(request):

	return render(request, 'bagify/account.html')

#Categories page
def collections(request, query = ''):

	categories = Category.objects.all().values()

	items_values = Item.objects.all().values()
	items_json = json.dumps(list(items_values), cls=DjangoJSONEncoder)

	items = Item.objects.all()

	return render(request, 'bagify/collections.html', {'categories': categories, 'query': query, 'items_json': items_json, 'items':items})


#Product page
def product(request, id):
	product = get_object_or_404(Item, pk=id)
	return render(request, 'bagify/product.html', {'product': product})


def cart(request):
	cookies = request.COOKIES.get('cart')
	if not cookies:
		return render(request, 'bagify/cart.html')

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

	return render(request, 'bagify/cart.html', {'cart': bigCart})

def checkout(request):

	return render(request, 'bagify/cart.html')



def view_that_asks_for_money(request, price, name, unique_id):

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
    context = {"form": form}
    return render(request, "payment.html", context)
