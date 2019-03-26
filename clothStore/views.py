from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.


def home(request):
	return render(request, 'cloth_store/index.html')

def collections(request):
	categories = Category.objects.all()
	item = Item.objects.first()
	print(item.images)

	return render(request, 'cloth_store/collections.html', {'categories': categories, 'item': item})


def indexCache(request):
	cache_key = 'indexPageData'
	cache_time = 21600
	data = cache.get(cache_key)

	if not data:
		my_service = Service()
		data = service.get_data()

	cache.set(cache_key, data, cache_time)

	return JsonResponse(data, safe=False)
