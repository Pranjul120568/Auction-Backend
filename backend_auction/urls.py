from backend import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/img-upload', views.img_upload.as_view()),
]
