from django.db import models
from django.contrib.auth.models import User  # You can customize the User model as needed for customers

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Add other restaurant-related fields like address, contact info, etc.

class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other customer-related fields like address, phone number, etc.

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    # Add payment-related fields like payment method, transaction ID, etc.
