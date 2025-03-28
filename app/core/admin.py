from django.contrib import admin

# Register your models here.
from django.apps import apps

# Register all models in the admin site
for model in apps.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass