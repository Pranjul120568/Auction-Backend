from django.contrib import admin
from .models import userprofile
# Register your models here.


@admin.register(userprofile)
class user_admin(admin.ModelAdmin):
    list_display = ['id', 'user', 'middle_name', 'dob',
                    'phone_number']
