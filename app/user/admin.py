from django.contrib import admin
from .models import UserProfile
from django.apps import apps


class UserAdmin(admin.AdminSite):
    site_header = "User Admin Area"


userAdmin = UserAdmin(name="UserAdmin")
userAdmin.register(UserProfile)


# Core Config for the Admin Site
for model in apps.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
