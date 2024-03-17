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
from django.contrib.auth import views as auth_views
from mainPage import views 
from mainPage.views import EditProfile

urlpatterns = [
    path('admin/', admin.site.urls), #admin dashboard
    path("superUserPage", views.superUserPage, name="superUserPage"),
    # path("edit_profile/", auth_views.PasswordChangeView.as_view(template_name="registration/edit_profile.html"), name="edit_profile"),
    path("edit_profile/", EditProfile.as_view(template_name="registration/edit_profile.html"), name="edit_profile"),
    path('', include("django.contrib.auth.urls")), # django will get to django.contrib.auth application and go to urls file

    #mainPage
    path("login_page/", views.loginPage, name="login_page"),
    path("register_page/", views.registerPage, name="register_page"),
    path("logout/", views.logoutUser, name="logout_page"),
    path("", views.home, name='home'), 
    path("about/", views.about, name="about"),
    path("product/<str:pk>/", views.product, name="product"), #pk is the dynamic url.
    path("cart/", views.cart, name="cart"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/done/<str:pk>/", views.checkout_done, name="checkout_done"),
    path("profile/", views.profile, name="profile"),

    path("updateItem/", views.updateItem, name="updateItem"),
    path("updateCartQuantity/", views.updateCartQuantity, name="updateCartQuantity"),
    path("updateCart/", views.updateCart, name="updateCart"),
    path("removeFromCartWishlist/", views.removeFromCartWishlist, name="removeFromCartWishlist"),
    path("paymentMethod/", views.paymentMethod, name="paymentMethod"),
    path("confirmOrder/", views.confirmOrder, name="confirmOrder"),
    path("load_cities/", views.load_cities, name="load_cities"),
    path("temp/", views.temp, name="temp"),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #add the path. static files. 2 arguments. 1 for the url and 1 from the root. 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#  path('<str:name>', include("list.urls")),

# path('', include("mainPage.urls")), #main url. Automatically directed to the list.urls file. Link this to urls.py in "list" application
    # path('about/', include("mainPage.urls")),
    # # path('product/<str:pk>/', include("mainPage.urls")),