from django.urls import path 
from .views import EventAndOffersAPIView, PlacesAPIView , SearchAPI

urlpatterns = [
    path('places/',PlacesAPIView.as_view()),
    path('events/',EventAndOffersAPIView.as_view()),
    path('search/',SearchAPI.as_view(), name ='search'),
]