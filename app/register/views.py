from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from website.models import Order, OrderDish, OrderStatus

def register(request):
    print(f"Mtd {request.method}")
    if request.method == "POST":
        form = RegisterForm(request.POST)
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

            if user.is_staff:
                return redirect("/admin")
            
            if is_chef(user):
                return redirect("/client/chef")

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
    order = Order.objects.filter(Q(status__id=1) | Q(status__id=2) | Q(status_id=4), customer=user).latest("created_at")
    order_status = OrderStatus.objects.get(id=2)

    if not order:
        order = Order.objects.create(customer=user, status=order_status)
    
    order_dish_count = OrderDish.objects.filter(order=order).count()
    request.session["order_count"] = order_dish_count
    request.session["order_id"] = order.id

def is_chef(user):
    try:
        user.groups.get(name="chef")
        return True
    except Group.DoesNotExist as e:
        print("Error: Group 'chef' does not exist!")
        return False
