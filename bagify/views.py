from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .utils import getCart, GetOrder, getTotal
from .models import *

from .forms import AddressForm


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
	cart = getCart(request)
	return render(request, 'bagify/cart.html', { 'cart': cart })

def checkout(request):
	total = getTotal(request)

	if request.method == 'POST':
		cookies = request.COOKIES.get('cart')
		cart = json.loads(cookies)

		response = json.loads(request.body)

		if request.user.is_anonymous:
			name = response.get('fullname')
			print(response.get('fullname'))
			user = None
		else:
			user = request.user
			name = ' '.join([user.firstname, user.lastname])

		if True:
			address = {
				'country': response.get('country'),
				'state': response.get('state'),
				'city': response.get('city'),
				'address': response.get('address'),
				'complement': response.get('complement'),
				'zip': response.get('zip'),
			}

			if response.get('save-address') == 'true' and not request.user.is_anonymous:
				model = Address(**address, user=request.user)
				model.save()

			text_address = ' - '.join(address.values())

		order = Order(address=text_address, status='Payment Pending', total=total, name=name, user=user, items=cart)
		order.save()

		return JsonResponse({'success': True, 'order-id': order.pk})

	else:
		addressForm = AddressForm()
		cart = getCart(request)
		return render(request, 'bagify/checkout.html', { 'cart': cart, 'addressForm': addressForm, 'total': total})

@csrf_exempt
def paypal_transaction_complete(request):
	if request.method == 'POST':
		order = json.loads(request.body)
		print(order)
		# GetOrder().get_order(order['orderID'])
	return HttpResponse(request, 'Hooray we got the money')
