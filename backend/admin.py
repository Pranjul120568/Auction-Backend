from django.contrib import admin
from .models import saved_products, product
# Register your models here.


# @admin.register(userprofile)
# class user_admin(admin.ModelAdmin):
#     list_display = ['id', 'user']


@admin.register(saved_products)
class saved_admin(admin.ModelAdmin):
    list_display = ['id', 'email', 'product_id', 'bidded']


@admin.register(product)
class saved_admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'cataegory', 'postedby',
                    'highest_bid', 'expire_time', 'posted_on', 'current_bidder']
