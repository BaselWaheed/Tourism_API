from django.contrib import admin
from .models import Offers, Turism  ,Places , Rate , Event



class TursimAdmin(admin.ModelAdmin):
    list_display = ['name' ]

admin.site.register(Turism,TursimAdmin)
########################################################################

class RateAdmin(admin.ModelAdmin):
    list_display = ['user','place' ,'rate']


admin.site.register(Rate,RateAdmin)
############################################################################
class PlacesAdmin(admin.ModelAdmin):
    list_display = ['place_name' , 'price', 'type' , 'is_active']
    list_filter = ['type']
    search_fields = ['place_name']

admin.site.register(Places,PlacesAdmin)

###########################################################################
class OffersAdmin(admin.ModelAdmin):
    list_display = ['place','new_price']


admin.site.register(Offers,OffersAdmin)

##########################################################################
class EventAdmin(admin.ModelAdmin):
    list_display = ['date_from','place' ,'date_to']

admin.site.register(Event,EventAdmin)


