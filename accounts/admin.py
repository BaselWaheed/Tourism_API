from django.contrib import admin
from .models import User , EmailAddress ,PhoneNumber
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", 'first_name' , 'username']
admin.site.register(User,UserAdmin)


class EmailAdmin(admin.ModelAdmin):
    list_display = ["id", 'user' , 'email']

admin.site.register(EmailAddress,EmailAdmin)



admin.site.register(PhoneNumber)