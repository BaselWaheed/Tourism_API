from .models import  Offers, Turism , Places , Event
from rest_framework.response import Response
from .serializers import EventSerializer, OffersSerializer, PlacesSerializer , TursimSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication




class PlacesAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        data = {"category":[]}
        products = {'places':[]}
        category = Turism.objects.all()
        category_serializer= TursimSerializer(category,many=True)
        for item in category_serializer.data :
            category = Turism.objects.get(name=item['name'])
            categoryfilter = Places.objects.filter(type=category.id)
            serializer = PlacesSerializer(categoryfilter,many=True)
            for product in serializer.data :
                products['places'].append(product)
            item['info']=products  
            data['category'].append(item)
            products = {'places':[]} 
        return Response({"status":True , "message":"working", "data": data}, status=status.HTTP_200_OK)     


        
class EventAndOffersAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        data = {"popular_places":[],"Top_Rated":[],"offers":[],"events":[]}
        places = Places.objects.filter(is_active=True)
        places_serializer = PlacesSerializer(places,many=True)
        for item in places_serializer.data:
            data["popular_places"].append(item)
            if item['rate'] >=3:
                data["Top_Rated"].append(item)
        offers = Offers.objects.all()
        offers_serializer = OffersSerializer(offers,many=True)
        for item in offers_serializer.data:
            data["offers"].append(item)
        event = Event.objects.all()
        event_serializer = EventSerializer(event,many=True)
        for item in event_serializer.data:
            data["events"].append(item)
        return Response({'status':True,"message":"null",'data':data})


class SearchAPI(ListCreateAPIView):
    # authentication_classes = (GuestAuthentication,)
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    def list(self, request, *args, **kwargs):
        data = {}
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data['places']=serializer.data
            return self.get_paginated_response({'status': True,'data':data})
        serializer = self.get_serializer(queryset, many=True)
        data['places']=serializer.data
        return Response({'status': True,'message':"working",'data':data})
    def post(self, request, *args, **kwargs):
        SearchAPI.queryset = Places.objects.filter(place_name__contains=request.data['place'])
        return self.list(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        return Response({'status':False , "message":"method GET not allowed"})