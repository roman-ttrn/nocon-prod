"""
URL configuration for nocon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from user.views import *
from .views import *

urlpatterns = [
    path('adm1n228qweEE/', admin.site.urls),
    path('home/', home, name='home'),
    path('user/', include('user.urls')),
    path('', include('core.urls')),
    path('chat/', include('chat.urls'), name='chat'),
    path('lists/', include('lists.urls')),
    path("search_suggestions/", search_suggestions, name="search_suggestions"),
    path('health/', health, name='health'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
