from django.contrib import admin
from .models import Restaurant, Dish, Employee

admin.site.register(Employee)

admin.site.register(Restaurant)

admin.site.register(Dish)
