"""TanpaTitik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from register import views as v 

urlpatterns = [
    path('admin/', admin.site.urls), #admin dashboard
    path('', include("mainPage.urls")), #main url. Automatically directed to the list.urls file. Link this to urls.py in "list" application
    path('about/', include("mainPage.urls")),
    path('register/', v.register, name="register"), # create a simple urls without urls from the application
    path('profile/', v.profile, name="profile"),
    path('', include("django.contrib.auth.urls")), # django will get to django.contrib.auth application and go to urls file
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #add the path. static files. 2 arguments. 1 for the url and 1 from the root. 

#  path('<str:name>', include("list.urls")),