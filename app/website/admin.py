from django.contrib import admin
from .models import Restaurant, Dish

admin.site.register(Restaurant)
admin.site.unregister(Restaurant)

admin.site.register(Dish)
admin.site.unregister(Dish)
