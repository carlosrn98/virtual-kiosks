from django.urls import path
from .views import home, restaurant

urlpatterns = [
    path("", home.index, name="index"),
    path("restaurants/", restaurant.RestaurantList.as_view(), name="restaurants")
]
