from django.contrib import admin
from .models import User , EmailAddress ,PhoneNumber
# Register your models here.
admin.site.register(User)



admin.site.register(EmailAddress)



admin.site.register(PhoneNumber)