from django.shortcuts import render
from .models import userprofile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import userserializer
from django.contrib.auth.hashers import make_password

# Create your views here.


class user_req(APIView):
    def get(self, request, format=None):
        user_details = userprofile.objects.get(id=1)
        if user_details.user.check_password("arora@123"):
            serializer = userserializer(user_details)
            return Response(serializer.data)
        else:
            return Response("MAa chuda")


# Documented
