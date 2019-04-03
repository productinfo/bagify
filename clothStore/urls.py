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
	path('paypal/', include('paypal.standard.ipn.urls')),
	path('payment_done', TemplateView.as_view(template_name='alert/payment_done.html'), name='payment_done'),
	path('payment_cancelled', TemplateView.as_view(template_name='alert/payment_cancelled.html'), name='payment_cancelled'),
	]
