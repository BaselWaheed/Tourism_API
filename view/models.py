from django.db import models
from accounts.models import User




class Turism(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


class Places(models.Model):
    classes =[
        ("A","A"),
        ("B","B"),
        ("C","C"),
    ]
    type = models.ForeignKey(Turism, on_delete=models.CASCADE)
    place_name =  models.CharField(max_length=50)
    Description = models.TextField()
    location = models.URLField()
    price_class = models.CharField(max_length=1,choices=classes)
    image = models.URLField()
    is_active = models.BooleanField(default=False)
    favourite_place = models.ManyToManyField(User, through='Favouriteplace')


    def __str__(self):
        return self.place_name


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    rate = models.FloatField()
    def __str__(self):
        return self.place.place_name


class Event(models.Model):
    event_name = models.CharField(max_length=100,null=True)
    event_image = models.URLField()
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField()
    discription = models.CharField( max_length=500)

    def __str__(self):
        return self.place.place_name




class Offers(models.Model):
    offer_name = models.CharField(max_length=100)
    place = models.OneToOneField(Places, on_delete=models.CASCADE)
    old_price =models.IntegerField()
    new_price =models.IntegerField()
    
    def __str__(self):
        return self.place.place_name



class Favouriteplace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default =False)


    def __str__(self):
        return self.user.username       




class Commenteplace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000,null=False)

    def __str__(self):
        return self.user.username      