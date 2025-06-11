# buyer/urls.py
from django.urls import path
from .views import BuyerDetailUpdateDelete 
from .views import BuyerDetailUpdateDelete, BuyerListCreateView

urlpatterns = [
    path('<str:phone_number>/', BuyerDetailUpdateDelete.as_view()),
    path('', BuyerListCreateView.as_view()),  # GET/POST
    path('<str:phone_number>/', BuyerDetailUpdateDelete.as_view()),
]
