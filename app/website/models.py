from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} - {self.description}"

class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} - {self.restaurant.name}"

class OrderStatus(models.Model):
    name = models.CharField(max_length=255)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, through='OrderDish')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(default=datetime.now)
    status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING)

class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
# g0od-p@ssw0rd