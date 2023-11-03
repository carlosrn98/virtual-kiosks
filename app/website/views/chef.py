from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.models import OrderStatus, OrderDish, Dish, Order, Employee
from django.contrib import messages
from website.utils import has_group

class ChefView:
    @login_required
    @has_group("chef")
    def chef_details(request):
        print(f"{request}")
        data = ChefView.get_order_dishes_by_restaurant(request.user.id)
        context = {"data": data}
        return render(request, "website/chef/order_detail.html", context)

    def get_order_dishes_by_restaurant(user_id):
        employee = Employee.objects.select_related("restaurant").filter(user__id=user_id)
        order_dish = OrderDish.objects.select_related("dish") \
                                      .select_related("status") \
                                      .select_related("dish__restaurant") \
                                      .filter(dish__restaurant=employee[0].restaurant)
        
        return order_dish

    @login_required
    @has_group("chef")
    def update_dish_status(request, *args, **kwargs):
        order_dish = OrderDish.objects.get(id=kwargs["orderdish_id"])
        order_dish.status_id = kwargs["status_id"]
        order_dish.save()

        return redirect("/client/chef")
