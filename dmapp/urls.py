from django.urls import path, include
from dmapp.views import HomeView, customerList

urlpatterns = [
    path('', HomeView, name='home'),
    path('customer-list/', customerList, name='customer-list')
]
