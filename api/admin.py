

from django.contrib import admin

from .models import User, Site, Product
from django.contrib import admin
admin.site.register(User)
admin.site.register(Site)
admin.site.register(Product)
