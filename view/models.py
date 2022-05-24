from django.db import models
from accounts.models import User




class Turism(models.Model):
    name = models.CharField(max_length=50)
    cat_image = models.URLField(null=True)
    favourite_category = models.ManyToManyField(User, through='InterrestCategory')

    def __str__(self):
        return self.name


class InterrestCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Turism, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default =False)

    
class City(models.Model):
    city_name = models.CharField(("city"), max_length=50)
    
    def __str__(self):
        return self.city_name

class Places(models.Model):
    classes =[
        ("A","A"),
        ("B","B"),
        ("C","C"),
    ]

    types =[
        ("Youths","Youths"),
        ("Adults","Adults"),
        ("All","All")]
    type = models.ForeignKey(Turism, on_delete=models.CASCADE)
    place_name =  models.CharField(max_length=50)
    city = models.ForeignKey(City, verbose_name=("city"), on_delete=models.CASCADE , null=True , blank=True)
    Description = models.TextField()
    location = models.URLField()
    price_class = models.CharField(max_length=1,choices=classes)
    age_category = models.CharField(max_length=30,choices=types)
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
    city = models.ForeignKey(City, verbose_name=("city"), on_delete=models.CASCADE , null=True)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    description = models.CharField( max_length=500)

    # def __str__(self):
    #     return self.city.city_name




class Offers(models.Model):
    offer_name = models.CharField(max_length=50)
    offer_description= models.TextField(null=True)
    offer_image = models.URLField(null=True)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
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