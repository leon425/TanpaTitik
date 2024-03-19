from django.contrib import admin
from .models import *

# general_models
admin.site.register(Additional)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Wishlist)
admin.site.register(Testimony)
admin.site.register(FAQs)
admin.site.register(Identity)
admin.site.register(Payment)
admin.site.register(OrderStatus)
admin.site.register(MeetTheTeam)

# product_models
admin.site.register(Products)
admin.site.register(Products_overview)
admin.site.register(Products_material)
admin.site.register(Products_review)
admin.site.register(Products_offer)
admin.site.register(Products_img)


# Register your models here.
