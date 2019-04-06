
def makeOrder():


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
	