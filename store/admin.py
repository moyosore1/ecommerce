from django.contrib import admin
from .models import *
import datetime
from django.utils.translation import gettext_lazy as _

# Register your models here.

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shipping)
admin.site.register(Category)
admin.site.register(Wishlist)