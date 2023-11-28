from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.models import OrderStatus, OrderDish, Dish, Order
from django.contrib.auth import get_user
from django.contrib import messages
from decimal import Decimal

class OrderView:
    @login_required
    def add_to_order(request, *args, **kwargs):
        dish = Dish.objects.get(id=kwargs["dish_id"])

        status = OrderStatus.objects.get(id=1)
        order = Order.objects.get(id=int(request.session.get("order_id")))

        order_dish = OrderDish.objects.create(order=order, dish=dish, status=status)
        request.session["order_count"] = request.session["order_count"] + 1
        
        messages.success(request, "Producto agregado")

        return redirect(f"{request.GET.get('page')}")

    @login_required
    def order_detail(request, pk):
        order_data = OrderDish.objects \
                    .select_related('order', 'dish', 'status') \
                    .filter(order_id=pk)

        total_price =  Decimal('0.00')
        is_order_ready_to_pay = True
        for row in order_data:
            if row.status_id != 3:
                total_price += row.dish.price 
            if row.status.id != 4:
                is_order_ready_to_pay = False
        
        if is_order_ready_to_pay and request.session["order_count"] > 0:
            order = Order.objects.filter(id=order_data[0].order.id).first()
            order.status_id = 4
            order.save()

        context = {"order_data": order_data,
                   "total": total_price,
                   "order_id": pk,
                   "is_order_ready_to_pay": is_order_ready_to_pay}
        return render(request, "website/order/order_detail.html", context)

    @login_required
    def remove_from_order(request, *args, **kwargs):
        order_dish = OrderDish.objects.get(id=int(kwargs["orderdish_id"]))
        order_dish.delete()

        if request.session["order_count"] > 0:
            request.session["order_count"] = request.session["order_count"] - 1
        
        messages.success(request, "Platillo eliminado exitosamente")

        return redirect(request.GET.get('page'))
