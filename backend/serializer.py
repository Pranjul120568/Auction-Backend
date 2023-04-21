from rest_framework import serializers
from .models import saved_products, product
from django.contrib.auth.models import User


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email', 'password')


# class user_serializer(serializers.ModelSerializer):
#     user = check_user_serializer(required=True)

#     class Meta:
#         model = userprofile
#         fields = ['user']


class savedproducts_serializer(serializers.ModelSerializer):
    class Meta:
        model = saved_products
        fields = ['id', 'email', 'product_id', 'bidded']


class product_serializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['id', 'name', 'price', 'cataegory', 'postedby',
                  'highest_bid', 'expire_time', 'posted_on', 'current_bidder']
