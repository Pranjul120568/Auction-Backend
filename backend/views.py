from django.shortcuts import render
from .models import product, saved_products
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import user_serializer, savedproducts_serializer, product_serializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import datetime
import jwt
from .send_token import get_token
from .authentication import is_logged_in
import time
# Create your views here.

# register user


class register_user(APIView):
    def post(self, request, format=None):
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        if password != confirm_password or confirm_password is None:
            return Response({'msg': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['password'] = make_password(request.data['password'])
        serializer = user_serializer(data=request.data)
        print(request.data['password'])
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        try:
            token = get_token(request.date['email'])
            # .decode('utf-8')
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt': token,
                'email': request.data['email'],
                'is_staff': False
            }
            return response
        except:
            return Response({'msg': 'User data not valid!'}, status=status.HTTP_400_BAD_REQUEST)
# login user


class login_user(APIView):
    def post(self, request, format=None):
        user_details = User.objects.get(email=request.data['email'])
        if not user_details.check_password(request.data['password']):
            return Response("Incorrect username or password")
        try:
            token = get_token(request.date['email'])
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt': token,
                'email': request.data['email'],
                'is_staff': False
            }
            return response
        except:
            return Response({'msg': 'User data not valid!'}, status=status.HTTP_400_BAD_REQUEST)
# update password


class update_password(APIView):
    def put(self, request, format=None):
        logged_in = is_logged_in(request)
        if not logged_in:
            raise AuthenticationFailed('Unauthenticated!')
        user_details = User.objects.get(email=request.data['email'])
        updated_password = make_password(request.data['password'])
        userserialize = user_serializer(
            user_details, data={'password': updated_password}, partial=True)
        if userserialize.is_valid():
            userserialize.save()
            return Response("Password Updated")
        return Response("Error updating password")

# get user details


class get_user_details(APIView):
    def get(self, request, format=None):
        logged_in = is_logged_in(request)
        if logged_in:
            try:
                user_details = User.objects.get(email=request.data['email'])
                serializer = user_serializer(user_details)
                return Response(serializer.data)
            except:
                return Response({'msg': 'Could not fetch'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise AuthenticationFailed('Unauthenticated!')
# all


class products(APIView):
    def get(self, request, pk=None, format=None):
        if pk is None:
            wished_product = product.objects.all()
        else:
            wished_product = product.objects.get(id=pk)
        try:
            serializer = product_serializer(wished_product, many=True)
            return Response(serializer.data)
        except:
            return Response({'msg': 'Could not fetch'})
# post a product, while posting
# import datetime
# datetime.date.today()  # Returns 2018-01-15
# datetime.datetime.now() # Returns 2018-01-15 09:00

    def post(self, request, format=None):
        pass

# posted by a user


class get_posted_products(APIView):
    def get(self, request, format=None):
        logged_in = is_logged_in(request)
        if not logged_in:
            raise AuthenticationFailed('Unauthenticated!')
        user_details = User.objects.get(email=request.data['email'])
        user_id = user_details.email
        wished_products = product.objects.filter(email=user_id)
        try:
            serializer = product_serializer(wished_products, many=True)
            return Response(serializer.data)
        except:
            return Response({'msg': 'Could not fetch'})

# place bid


class create_bid(APIView):
    def post(self, request, format=None):
        logged_in = is_logged_in(request)
        if not logged_in:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['email']
        bid = request.data['price']
        product_details = product.objects.get(id=request.data['id'])
        if product_details.highest_bid > price:
            return Response({'msg': 'Price is too low!!'})
        if product_details.expire_time < time.time():
            return Response({'msg': 'Auction has ended'})
        updated_bid = {
            "highest_bid": bid,
            "current_bidder": user_id
        }
        new_saved_product = {
            "product_id": request.data['id'],
            "email": user_id,
            "bidded": True
        }
        try:
            already_placed = saved_products.objects.filter(
                product_id=request.data['id'], email=user_id)
            if already_placed is None:
                serialized_saved_product = savedproducts_serializer(
                    data=new_saved_product)
            else:
                serialized_saved_product = savedproducts_serializer(
                    already_placed, data=new_saved_product, partial=True)

            serialized_product = product_serializer(
                product_details, data=updated_bid, partial=True)
            if serialized_product.is_valid() and serialized_saved_product.is_valid():
                serialized_product.save()
                serialized_saved_product.save()
        except:
            return Response({'msg': 'Cannot place bid error occured'})


# bidded/saved upon by a user
class saved_products(APIView):
    def get(self, request, format=None):
        logged_in = is_logged_in(request)
        if not logged_in:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['email']
        try:
            all_saved = saved_products.objects.filter(email=user_id)
            serialized_saved = savedproducts_serializer(all_saved)
            return Response(serialized_saved.data)
        except:
            return Response({'msg': 'Sorry could not fetch products'})


class delete_saved_products(APIView):
    def delete(self, request, pk=None):
        logged_in = is_logged_in(request)
        if not logged_in:
            raise AuthenticationFailed('Unauthenticated!')
        saved_one = saved_products.objects.get(id=pk)
        if request.data['email'] != saved_one.email or saved_one.bidded == True:
            return Response({'msg': "Cannot delete Sorry"})
        try:
            saved_one.delete()
            return Response({'msg': "Deleted!!"})
        except:
            return Response({'msg': "Some error Occured"})

# >>> import datetime
# >>> orig = datetime.datetime.fromtimestamp(1425917335)
# >>> new = orig + datetime.timedelta(days=90)
# >>> print(new.timestamp())
# 1433693335.0
# import the time module


# get the current time in seconds since the epoch
