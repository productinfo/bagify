from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('collections/', views.collections, name='collections'),
]
