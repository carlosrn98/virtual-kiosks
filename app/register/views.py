from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from website.models import Order, OrderDish, OrderStatus

def register(request):
    print(f"Mtd {request.method}")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print(f"LLEGO: {request.body} VALID: {form.is_valid()}")
        if form.is_valid():
            form.save()
            return redirect("/login")
        else:
            messages.error(request, "Vuelve a enviar tus datos correctamente")
    
    form = RegisterForm()

    return render(request, "register/register.html", {"form":form})

def login_user(request):
    form = AuthenticationForm(data=request.POST)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pswd")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            create_order(request, user)
            return redirect('/client')
        else:
            print("FALLIDO")
            messages.error(request, "Login fallido")
    return render(request, "register/login.html", {"form":form})

def logout_user(request):
    logout(request)
    return redirect('/client')

def create_order(request, user):
    order = Order.objects.filter(customer=user, status__id__lt=3).first()
    order_status = OrderStatus.objects.get(id=2)

    if not order:
        order = Order.objects.create(customer=user, status=order_status)
    
    order_dish = OrderDish.objects.filter(order=order).count()
    print(f"COUNT: {order_dish}, ORDER ID: {order.id}")
    request.session["order_count"] = order_dish
    request.session["order_id"] = order.id
