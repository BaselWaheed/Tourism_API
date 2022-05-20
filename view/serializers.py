from rest_framework import serializers
from .models import Commenteplace, Favouriteplace, InterrestCategory, Offers, Turism , Places , Rate , Event 



class PlacesSerializer(serializers.ModelSerializer):
    type =  serializers.StringRelatedField()
    rate = serializers.SerializerMethodField()
    in_favourite = serializers.SerializerMethodField()
    city =  serializers.StringRelatedField()
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
        fields = ['id','place_name','type','age_category','Description','city','price_class','location','image','is_active','rate','in_favourite']


class TursimSerializer(serializers.ModelSerializer):
    in_favourite = serializers.SerializerMethodField()

    def get_in_favourite(self,obj):
        try:
            favourite = InterrestCategory.objects.filter(user=self.context['request'].user).filter(category_id=obj.id)
            if favourite  :
                return True
            else :
                return False
        except :
            return False
    class Meta:
        model = Turism
        fields = ['id','name','cat_image','in_favourite']



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

