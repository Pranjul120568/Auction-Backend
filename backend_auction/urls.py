from backend import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/img-upload', views.img_upload.as_view()),
    path('register', views.register_user.as_view()),
    path('login', views.login.as_view()),
    path('getuser', views.get_user_details.as_view()),
    path('getproducts/<int:pk>', views.getproduct.as_view()),
    path('user_products', views.get_posted_products.as_view()),
    path('postproducts', views.postproduct.as_view()),
    path('createBid', views.create_bid.as_view()),
    path('usersavedproducts', views.saved_products.as_view()),
    path('removesavedproducts', views.remove_saved_products.as_view()),

]
