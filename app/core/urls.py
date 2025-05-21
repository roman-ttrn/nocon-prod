from django.urls import path, include

from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('delete_post/<int:pk>/', delete_post, name='delete_post'),
    path('certain_post/<int:post_id>/', certain_post, name='certain_post'),
]
