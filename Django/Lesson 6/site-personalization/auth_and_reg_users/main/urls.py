"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include

import auth.views

urlpatterns = [
    path('', auth.views.home),
    path('admin/', admin.site.urls),
    path('home/', auth.views.home, name='home'),
    path('signup/', auth.views.signup, name='signup'),
    path('login/', auth.views.auth_login, name='auth_login'),
    path('logout/', auth.views.logout_view, name='logout_view'),
    path('password_reset/', auth.views.password_reset, name='password_reset'),
    #path('', include('django.contrib.auth.urls'))
]
