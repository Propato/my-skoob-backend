from django.contrib import admin
from .models import UserProfile

class UserAdmin(admin.AdminSite):
    site_header = 'User Admin Area'

userAdmin = UserAdmin(name='UserAdmin')
userAdmin.register(UserProfile)