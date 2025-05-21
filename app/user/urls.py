from django.urls import path, include
from .views import *

urlpatterns = [
    path('login_user/', login_user, name='login_user'),
    path('confirm_email/', confirm_email, name='confirm_email'),
    path('logout_user/', logout_user, name='logout_user'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile')
]
