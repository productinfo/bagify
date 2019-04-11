from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .utils import getCart, GetOrder, getTotal, getOrderDetails, addAddress
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
	if request.method == 'POST':
		response = json.loads(request.body)
		if response['type'] == 'address':
			if response['action'] == 'remove':
				address = Address.objects.get(pk=response['id'])
				if(address.user == request.user):
					address.delete()
				else:
					return JsonResponse({'success': False})
			elif response['action'] == 'add':
				response['save-address'] = 'true'
				address = addAddress(response, request)
				return JsonResponse({'success': True, 'id': address['id']})
		elif response['type'] == 'change_password':
			if request.user.check_password(response['current_pas']):
				print('yep')
		elif response['type'] == 'delete_account':
			pass
		return JsonResponse({'success': True})
	addressForm = AddressForm()
	return render(request, 'bagify/account.html', {'addressForm': addressForm})

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
	addressForm = AddressForm()
	cart = getCart(request)
	return render(request, 'bagify/checkout.html', { 'cart': cart, 'addressForm': addressForm, 'total': total})

@csrf_exempt
def paypal_transaction_complete(request):
	if request.method == 'POST':
		response = json.loads(request.body)
		answer = GetOrder().get_order(response['orderID'], response['addressDetails'], request)

		if(answer == 0):
			return JsonResponse({'success':True})

	return render(request, 'bagify/transaction_completed.html')

def order(request, id):
	orderDetails = getOrderDetails(id)
	print(orderDetails)
	return JsonResponse(orderDetails)
