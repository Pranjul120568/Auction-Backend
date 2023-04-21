from django.db import models
# from django.contrib.auth.models import User
# Create your models here.


# class userprofile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class saved_products(models.Model):
    email = models.EmailField(max_length=254)
    product_id = models.IntegerField()
    bidded = models.BooleanField(default=False)


class product(models.Model):
    name = models.CharField(max_length=35, null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=200)
    cataegory = models.CharField(max_length=35)
    image = models.CharField(max_length=200)
    postedby = models.EmailField(max_length=254)
    highest_bid = models.IntegerField()
    expire_time = models.DateTimeField()
    posted_on = models.DateTimeField()
    current_bidder = models.EmailField(max_length=254, null=True)
