from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('characters/', characters, name='characters'),
    path('characters/create/', create_character, name='character_create'),
    path('plans/', plans, name='plans'),
    path('plans/create/', plan_create, name='plan_create'),
]