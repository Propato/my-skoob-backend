from django.urls import path
from .views import get_all_users, login_user, create_user, user_details
from .admin import userAdmin

urlpatterns = [
    path('', get_all_users, name='get_all_users'),
    path('login/', login_user, name='login_user'),
    path('create/', create_user, name='create_user'),
    path('details/', user_details, name='user_details'), # Get User, Update User, Delete User

    path('admin/', userAdmin.urls),
]