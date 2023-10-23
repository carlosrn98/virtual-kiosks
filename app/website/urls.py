from django.urls import path
from .views import home, restaurant, order

urlpatterns = [
    path("", home.index, name="index"),
    path("restaurants/", restaurant.RestaurantList.as_view(), name="restaurants"),
    path("restaurants/<int:pk>/dishes", restaurant.RestaurantDetail.handle_request, name="restaurant_detail"),
    path("restaurants/<int:restaurant_id>/dishes/<int:dish_id>/add", order.OrderView.add_to_order, name="add_to_order"),
    path("orders/<int:pk>", order.OrderView.order_detail, name="order_detail")
]
