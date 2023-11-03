from django.urls import path
from .views import home, restaurant, order, chef

urlpatterns = [
    path("", home.index, name="index"),
    path("restaurants/", restaurant.RestaurantList.as_view(), name="restaurants"),
    path("restaurants/<int:pk>/dishes", restaurant.RestaurantDetail.handle_request, name="restaurant_detail"),
    path("restaurants/<int:restaurant_id>/dishes/<int:dish_id>/add", order.OrderView.add_to_order, name="add_to_order"),
    path("orders/<int:order_id>/dish/<int:orderdish_id>/remove", order.OrderView.remove_from_order, name="remove_from_order"),
    path("orders/<int:pk>", order.OrderView.order_detail, name="order_detail"),
    path("chef/", chef.ChefView.chef_details, name="chef_detail"),
    path("chef/order-dish/<int:orderdish_id>/status/<int:status_id>/update", chef.ChefView.update_dish_status, name="orderdish_status_update")
]
