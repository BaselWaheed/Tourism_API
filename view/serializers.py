from rest_framework import serializers

from .models import Offers, Turism , Places , Rate , Event



class PlacesSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

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



    class Meta:
        model = Places
        fields = ['place_name','Description','location','price','comment','image','is_active','rate']


class TursimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turism
        fields = ['name']



class EventSerializer(serializers.ModelSerializer):
    date_from = serializers.DateTimeField(format="%d, %b %Y - %I:%M %p")
    date_to = serializers.DateTimeField(format="%d, %b %Y - %I:%M %p")

    class Meta:
        model = Event
        fields = ['date_from','date_to','discription','place']
        depth = 1

class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'
        depth = 1