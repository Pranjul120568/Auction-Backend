from rest_framework import serializers
from .models import userprofile
from django.contrib.auth.models import User


class CheckUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'is_staff')
# is staff check


class user_serializer(serializers.ModelSerializer):
    user = CheckUserSerializer(required=True)

    class Meta:
        model = userprofile
        fields = ['user', 'middle_name', 'dob', 'phone_number']
