from django.contrib import admin
from .models import Product, UserProfile, Order

admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Order)
