from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
	path('', views.home, name='home'),
	path('product/<int:id>/', views.product, name='product'),
	path('collections/<str:query>/', views.collections, name='collection'),
	path('collections/', views.collections, name='collections'),
	path('account/', views.account, name='account'),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.checkout, name='checkout'),

	path('paypal-transaction-complete', views.paypal_transaction_complete, name='paypal_complete')
	]
