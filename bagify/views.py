from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.conf import settings

from .utils import getCart, give_me_money_paypal
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
	cart = getCart(request)
	return render(request, 'bagify/cart.html', { 'cart': cart })

def checkout(request):
	cart = getCart(request)

	paypal = give_me_money_paypal(request, "10.00","a bag ", "cool bags")
	print(paypal)
	return render(request, 'bagify/checkout.html', { 'cart': cart, "paypal": paypal })



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
