from django.views.generic import ListView, DeleteView
from django.http import HttpResponse
from website.models import Restaurant

class RestaurantList(ListView):
    model = Restaurant
    context_object_name = "restaurant_list"
    template_name = "website/restaurant/restaurant_list.html"
