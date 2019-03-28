from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core.cache import cache
# Create your views here.


def home(request):
	carousel = CarouselImage.objects.all()
	mostPopular = Item.objects.order_by('-sold_units')[:8]
	newestAdditions = Item.objects.order_by('-id')[:8]

	print(mostPopular)
	return render(request, 'cloth_store/index.html', {'carousel': carousel, 'newest': newestAdditions, 'popular': mostPopular})

def account(request):
	return render(request, 'cloth_store/account.html')

def collections(request):
	categories = Category.objects.all()

	return render(request, 'cloth_store/collections.html', {'categories': categories, 'item': item})

def cart(request):

	return render(request, 'cloth_store/cart.html')


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

def addItem(request):
	if request.method == 'POST':
		if not request.user.cart:
			Cart.objects.create(user=request.user)

		request.user.cart.addItem(request.theItemId) # FIXME: Find where in the request will be the item id

def findItems(itemsIds):
	items = allItems();

	found = []
	notFound = []

	for item in itemsIds:
		if item in saf:
			dsf
