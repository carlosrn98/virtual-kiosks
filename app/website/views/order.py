from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.models import OrderStatus, OrderDish, Dish, Order
from django.contrib import messages

class OrderView:
    @login_required
    def add_to_order(request, *args, **kwargs):
        dish = Dish.objects.get(id=kwargs["dish_id"])

        status = OrderStatus.objects.get(id=1)
        order = Order.objects.get(id=int(request.session.get("order_id")))

        order_dish = OrderDish.objects.create(order=order, dish=dish, status=status)
        request.session["order_count"] = request.session["order_count"] + 1
        
        messages.success(request, "Platillo agregado")

        return redirect(f"{request.GET.get('page')}")

    @login_required
    def order_detail(request, pk):
        print(f"PK {pk}")
        order_data = OrderDish.objects \
                    .select_related('order', 'dish', 'status') \
                    .filter(order_id=pk)
        total_price = sum(row.dish.price for row in order_data)
        context = {"order_data": order_data,
                   "total": total_price,
                   "status": order_data[0].status.name}
        return render(request, "website/order/order_detail.html", context)

    @login_required
    def remove_from_order(request, *args, **kwargs):
        print(kwargs)
        order_dish = OrderDish.objects.get(id=int(kwargs["orderdish_id"]))
        order_dish.delete()

        if request.session["order_count"] > 0:
            request.session["order_count"] = request.session["order_count"] - 1
        
        messages.success(request, "Platillo eliminado exitosamente")

        return redirect(request.GET.get('page'))
