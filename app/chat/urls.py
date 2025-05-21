from django.urls import path

from .views import *

urlpatterns = [
    path('chat_list/', chat_list, name='chat_list'),
    path('<uuid:room_id>', chat, name='chat'),
    path('<uuid:room_id>/load-messages/', load_messages, name='load_messages'),
    path('users_list/', users_list, name='users_list'),
    path('add_chat/', add_chat, name='add_chat'),

]
