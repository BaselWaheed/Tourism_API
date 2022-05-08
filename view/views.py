from django.http import JsonResponse
from .models import Favouriteplace, Offers, Turism , Places , Event , Commenteplace , Rate
from rest_framework.response import Response
from .serializers import CommentSerializer, EventSerializer, OffersSerializer, PlacesSerializer , TursimSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view





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
            serializer = PlacesSerializer(categoryfilter,many=True,context={"request":request})
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
        data = {"popular_places":[],"Top_Rated":[],"offers":[],"events":[],"places":[]}
        places = Places.objects.all()
        place = places.filter(is_active=True)
        place_serializer = PlacesSerializer(place,many=True,context={"request":request})
        for item in place_serializer.data:
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
        places_serializer = PlacesSerializer(places,many=True,context={"request":request})
        for item in places_serializer.data:
            data["places"].append(item)
        return Response({'status':True,"message":"null",'data':data},status=status.HTTP_200_OK)


# class SearchAPI(ListCreateAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Places.objects.all()
#     serializer_class = PlacesSerializer
#     def list(self, request, *args, **kwargs):
#         data = {}
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             data['places']=serializer.data
#             return self.get_paginated_response({'status': True,'data':data})
#         serializer = self.get_serializer(queryset, many=True)
#         data['places']=serializer.data
#         return Response({'status': True,'message':"working",'data':data})
#     def post(self, request, *args, **kwargs):
#         SearchAPI.queryset = Places.objects.filter(place_name__contains=request.data['place'])
#         return self.list(request, *args, **kwargs)
#     def get(self, request, *args, **kwargs):
#         return Response({'status':False , "message":"method GET not allowed"})


class SearchAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self,request,**kwargs):
        data= {"places":[]}
        try :
            query = request.data['place']
        except:
            return Response({'status':False , "message":"enter place"},status=status.HTTP_200_OK)
        place_name = Places.objects.all()
        event_name = Event.objects.all()
        offer_name = Offers.objects.all()
        if query:
            place_name = place_name.filter(place_name__icontains=query)
            event_name = event_name.filter(event_name__icontains=query)
            offer_name = offer_name.filter(offer_name__icontains=query)
        event_serializer=EventSerializer(instance=event_name, many=True).data
        place_serializer = PlacesSerializer(instance=place_name, many=True).data
        offer_serializer = OffersSerializer(instance=offer_name, many=True).data
        for item in event_serializer:
            data['places'].append(item)
        for item in place_serializer :
            data['places'].append(item)
        for item in offer_serializer :
            data['places'].append(item)
        return Response({'status':True , "message":"working","data":data},status=status.HTTP_200_OK)

# @api_view(['GET', 'POST'])
# def view(request):
#     data= {"places":[]}
#     # query = request.data['place']
#     query = ''
#     place_name = Places.objects.all()
#     event_name = Event.objects.all()
#     offer_name = Offers.objects.all()
#     if query:
#         place_name = place_name.filter(place_name__icontains=query)
#         event_name = event_name.filter(event_name__icontains=query)
#         offer_name = offer_name.filter(offer_name__icontains=query)
#     event_serializer=EventSerializer(instance=event_name, many=True).data
#     place_serializer = PlacesSerializer(instance=place_name, many=True).data
#     offer_serializer = OffersSerializer(instance=offer_name, many=True).data
#     for item in event_serializer:
#         data['places'].append(item)
#     for item in place_serializer :
#         data['places'].append(item)
#     for item in offer_serializer :
#         data['places'].append(item)
#     return JsonResponse({"status":True,"message":"working","data":data})


class GetAddOrDeleteFavouriteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        data = {}
        query = Places.objects.filter(favourite_place=self.request.user)
        serializers = PlacesSerializer(query, many=True,context={"request":request})
        if serializers is None :
            return Response({'status':False , 'messege' : 'no favourite' })  
        else :
            data['places']= serializers.data
            return Response({'status':True , 'messege' : 'anta kda tmam' , 'data': data },status=status.HTTP_200_OK)
    def post(self,request):
        try :
            place = Places.objects.get(id=int(request.data['place_id']))
        except :
            return Response({'status': False,'message': 'please enter place_id correctly'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user  not in place.favourite_place.all():
            Favouriteplace.objects.create(user=self.request.user, place=place ,is_favourite=True) 
            return Response({'status': True,'message': 'place added to favourite'}, status=status.HTTP_200_OK)
        elif  request.user in place.favourite_place.all():
            place.favourite_place.remove(request.user)
            return Response({'status': True,'message': 'place removed from favourite'}, status=status.HTTP_200_OK)



class GetAddOrDeleteCommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        try :
            place = Places.objects.get(id=int(request.data['place_id']))
        except:
            return Response({'status': False,'message': 'Error data '}, status=status.HTTP_200_OK)
        Commenteplace.objects.create(user=self.request.user, place=place ,comment=request.data['comment']) 
        return Response({'status': True,'message': 'comment added successfully'}, status=status.HTTP_200_OK)


    def put(self,request,**kwargs):
        try :
            comment = Commenteplace.objects.get(pk=int(request.data.get('comment_id')))
        except :
            return Response({'status': False,'message': 'please enter comment_id correctly'}, status=status.HTTP_400_BAD_REQUEST)
        if comment.user == request.user:
            comment.comment = request.data['comment']
            comment.save()
            return Response({'status': True,'message': 'comment updated successfully'}, status=status.HTTP_200_OK)
        else :
            return Response({'status': False,'message': 'can not update comment'}, status=status.HTTP_400_BAD_REQUEST)




class PLaceDetailsAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        data = {}
        comments ={"comments":[]}
        try :
            place = Places.objects.get(id=int(request.data['place_id']))
            comment =Commenteplace.objects.filter(place=int(request.data['place_id']))
        except:
            return Response({'status': False,'message': 'please enter place_id'}, status=status.HTTP_400_BAD_REQUEST)
        place_serializer = PlacesSerializer(place,context={"request":request})
        comment_serializer = CommentSerializer(comment, many=True)
        for comment in comment_serializer.data:
            comments['comments'].append(comment)
        data.update(place_serializer.data)
        data.update(comments)
        return Response({'status': True,'message': 'null',"data":data}, status=status.HTTP_200_OK)
    

class AddRateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        try :
            place = Places.objects.get(id=int(request.data['place_id']))
        except:
            return Response({'status': False,'message': 'please enter place_id'}, status=status.HTTP_400_BAD_REQUEST)
        if Rate.objects.filter(user=self.request.user , place=place):
            user_rate = Rate.objects.get(user=self.request.user , place=place)
            user_rate.rate = request.data['rate']
            user_rate.save()
            return Response({'status': True,'message': 'rate updated to place successfully'}, status=status.HTTP_200_OK)
        Rate.objects.create(user=self.request.user, place=place ,rate=request.data['rate']) 
        return Response({'status': True,'message': 'rate added to place successfully'}, status=status.HTTP_200_OK)
