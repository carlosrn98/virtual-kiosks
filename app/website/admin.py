from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Restaurant, Dish, Employee
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django import forms

admin.site.site_title = "Virtual Kiosks"
admin.site.site_header = "VK Admin"

try:
    admin.site.unregister(User)
except:
    pass

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, **kwargs)
        
        if not request.user.is_superuser:
            disabled_fields = {"is_superuser", "user_permissions", "groups", "is_staff", "is_active", "username", "email", "password"}
            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True
        
        return form
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.is_superuser:
            return super().get_queryset(request)
        employee = Employee.objects.filter(user__id=request.user.id).first()
        qs = super().get_queryset(request).filter(is_staff=False)
        
        return qs

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        admin_group = Group.objects.get(name="admin_restaurant")
        password = make_password("g0od-p@ssw0rd")

        try:
            with transaction.atomic():
                user = User.objects.create(username=f"admin-{obj.name}", password=password, email=f"{obj.name}@gmail.com", is_staff=True)
                user.groups.add(admin_group)
                restaurant = Restaurant.objects.create(name=obj.name, description=obj.description)
                employee = Employee.objects.create(restaurant=restaurant, user=user)
        except Exception as e:
            print(f"There was a problem inserting data into DB after creating Restaurant: {e}")

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].queryset = Restaurant.objects.none()


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    # form = DishForm
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.is_superuser:
            return super().get_queryset(request)
        employee = Employee.objects.filter(user__id=request.user.id).first()
        qs = super().get_queryset(request).filter(restaurant__id=employee.restaurant.id)

        return qs
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        employee = Employee.objects.filter(user__id=request.user.id).first()
        rest = Restaurant.objects.get(id=employee.restaurant_id)
        Dish.objects.create(name=obj.name, description=obj.description, price=obj.price, restaurant=rest)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.is_superuser:
            return super().get_queryset(request)
        employee = Employee.objects.filter(user__id=request.user.id).first()
        qs = super().get_queryset(request).filter(restaurant__id=employee.restaurant.id)

        return qs

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        employee = Employee.objects.get(user_id=request.user.id)
        rest = Restaurant.objects.get(id=employee.restaurant_id)
        Employee.objects.create(user=obj.user, restaurant=rest)
