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
	mostPopular = Item.objects.order_by('-sold_units')[:8]
	newestAdditions = Item.objects.order_by('-id')[:8]
	categories = Category.objects.all()

	return render(request, 'cloth_store/index.html', {'carousel': carousel, 'newest': newestAdditions, 'popular': mostPopular, 'categories': categories })


#Account Page
def account(request):
	return render(request, 'cloth_store/account.html')

#Categories page
def collections(request, query = ''):

	categories = Category.objects.all().values()
	items = Item.objects.all().values()
	items_json = json.dumps(list(items), cls=DjangoJSONEncoder)

	return render(request, 'cloth_store/collections.html', {'categories': categories, 'query': query, 'items': items_json})


#Product page
def product(request, id):
	product = get_object_or_404(Item, pk=id)

	return render(product, 'cloth_store/product.html', {'product': product})


def cart(request):
	return render(request, 'cloth_store/cart.html')

def checkout(request):

	return render(request, 'cloth_store/cart.html')



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
