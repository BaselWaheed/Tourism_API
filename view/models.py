from django.db import models
from accounts.models import User




class Turism(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


class Places(models.Model):
    type = models.ForeignKey(Turism, on_delete=models.CASCADE)
    place_name =  models.CharField(max_length=50)
    Description = models.TextField()
    location = models.URLField()
    price = models.IntegerField()
    comment = models.CharField(max_length=500)
    image = models.URLField()
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.place_name


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    rate = models.IntegerField()
    def __str__(self):
        return self.place.place_name


class Event(models.Model):
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField()
    discription = models.CharField( max_length=500)

    def __str__(self):
        return self.place.place_name


class Offers(models.Model):
    place = models.OneToOneField(Places, on_delete=models.CASCADE)
    new_price =models.IntegerField()
    def __str__(self):
        return self.place.place_name