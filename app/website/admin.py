from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Restaurant, Dish, Employee

# admin.site.register(Employee)

admin.site.register(Restaurant)

admin.site.register(Dish)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if request.user.is_superuser:
            return super().get_queryset(request)
        employee = Employee.objects.filter(user__id=request.user.id).first()
        print(f"employee {employee}")
        qs = super().get_queryset(request).filter(restaurant__id=employee.restaurant.id)

        return qs
