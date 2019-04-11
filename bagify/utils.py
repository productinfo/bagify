import json

from django.conf import settings
from django.urls import reverse
from django.core import serializers

from .hooks import PayPalClient
from .models import *

from paypalcheckoutsdk.orders import OrdersGetRequest

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

def getTotal(request):
		cookies = request.COOKIES.get('cart')
		if not cookies:
			return 0

		cart = json.loads(cookies)
		total = 0

		for product in cart:
			item = Item.objects.filter(pk=product['id'])[0]
			if not item:
				continue
			total = total + float(item.price)

		return total

class GetOrder(PayPalClient):

#2. Set up your server to receive a call from the client
	"""You can use this function to retrieve an order by passing order ID as an argument"""
	def get_order(self, order_id, addressDetails, request):
		"""Method to get order"""

		if request.user.is_anonymous:
			user = None
			name = addressDetails['fullname']
		else:
			user = request.user
			name = ' '.join([user.first_name, user.last_name])


		total = getTotal(request)
		cart = request.COOKIES.get('cart')
		address = getAddress(json.loads(addressDetails), request)

		print(address, cart, total)

		request = OrdersGetRequest(order_id)
		#3. Call PayPal to get the transaction
		response = self.client.execute(request)
		#4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.

		print('Status Code: ', response)
		print('Status: ', response.result)
		print('Order ID: ', response.result.id)
		print('Intent: ', response.result.intent)
		print('Links:')
		for link in response.result.links:
			print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
		print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code, response.result.purchase_units[0].amount.value))

		print(float(total) == float(response.result.purchase_units[0].amount.value))

		if not address or not cart or not total or not name or not user:
			return 5

		if response.status_code != 200:
			return 4

		if float(total) != float(response.result.purchase_units[0].amount.value):
			return 1


		if response.result.purchase_units[0].amount.currency_code != 'USD':
			return 3

		order = Order(address=address, status='Order Confirmed', total=total, name=name, user=user, items=cart)
		order.save()

		return 0

def getAddress(addressDetails, request):

	if 'select' in addressDetails and addressDetails['select']:
		id = addressDetails['addressId']
		address_values = Address.objects.filter(pk=id).values()[0]
		text_address = json.dumps(address_values)

	else:
		print(addressDetails)
		address = addAddress(addressDetails, request)

		text_address = json.dumps(address['address_dict'])

	return text_address

def addAddress(addressDetails, request):
	address = {
		'country': addressDetails['country'],
		'state': addressDetails['state'],
		'city': addressDetails['city'],
		'address': addressDetails['address'],
		'complement': addressDetails['complement'],
		'zip': addressDetails['zip'],
	}
	if 'save-address' in addressDetails and addressDetails['save-address'] == 'true' and request.user.is_authenticated:
		model = Address(**address, user=request.user)
		model.save()
		return { 'address_dict' : address, 'id': model.pk}

	return {'address_dict': address}

def getOrderDetails(id, request):
	order = Order.objects.get(pk=id)
	if order.user != request.user:
		return ''


	orderData = {
		'id': order.id,
		'status': order.status,
		'total': float(order.total),
		'date': str(order.date.strftime("%A %d. %B %Y")),
		'items': []

	}

	address = json.loads(order.address)
	orderData['address'] = ', '.join([address['address'], address['complement'], address['zip']])

	for item in json.loads(order.items):
		model = Item.objects.get(pk=item['id'])
		data = {
			'color': item['color'],
			'name': model.name,
			'price': float(model.price),
		}
		orderData['items'].append(data)

	return orderData
