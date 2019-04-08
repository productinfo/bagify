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
	if request.method == 'POST':
		pass
	else:
		cart = getCart(request)
		total = getTotal(request)
		addressForm = AddressForm()

		return render(request, 'bagify/checkout.html', { 'cart': cart, 'addressForm': addressForm, 'total': total})

@csrf_exempt
def paypal_transaction_complete(request):
	if request.method == 'POST':
		order = json.loads(request.body)
		total = getTotal(request)

		GetOrder().get_order(order['orderID'], total)
	return HttpResponse(request, 'Hooray')
