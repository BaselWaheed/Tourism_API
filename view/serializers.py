from rest_framework import serializers
from .models import Commenteplace, Favouriteplace, Offers, Turism , Places , Rate , Event 



class PlacesSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    in_favourite = serializers.SerializerMethodField()
    def get_rate(self,obj):
        rate_value = 0
        count = 0
        place = Rate.objects.filter(place=obj)
        if place :
            for item in place :
                rate_value += item.rate
                count+=1
            return rate_value/count
        else :
            return 2

    def get_in_favourite(self,obj):
        try:
            favourite = Favouriteplace.objects.filter(user=self.context['request'].user).filter(place_id=obj.id)
            if favourite  :
                return True
            else :
                return False
        except :
            return False
        


    class Meta:
        model = Places
        fields = ['id','place_name','Description','location','image','is_active','rate','in_favourite']


class TursimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turism
        fields = ['name']



class EventSerializer(serializers.ModelSerializer):
    date_from = serializers.DateTimeField(format="%d, %b %Y - %I:%M %p")
    date_to = serializers.DateTimeField(format="%d, %b %Y - %I:%M %p")

    class Meta:
        model = Event
        fields = ['event_name','event_image','date_from','date_to','place','discription']
        depth = 1

class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Commenteplace
        fields = ['id','user','comment']

