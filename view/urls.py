from django.urls import path 
from .views import EventAndOffersAPIView, PlacesAPIView , SearchAPI , GetAddOrDeleteFavouriteView , GetAddOrDeleteCommentView ,PLaceDetailsAPIView,AddRateAPIView

urlpatterns = [
    path('places/',PlacesAPIView.as_view()),
    path('events/',EventAndOffersAPIView.as_view()),
    path('search/',SearchAPI.as_view(), name ='search'),
    path('favouriteplace/',GetAddOrDeleteFavouriteView.as_view() , name = 'favourite'),
    path('comment/',GetAddOrDeleteCommentView.as_view(),),
    path('details/',PLaceDetailsAPIView.as_view(),),
    path('rate/',AddRateAPIView.as_view(),),
]