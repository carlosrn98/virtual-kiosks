from django.views.generic import ListView, DeleteView
from django.http import HttpResponse
from website.models import Restaurant, Dish
from django.shortcuts import render


class RestaurantList(ListView):
    model = Restaurant
    context_object_name = "restaurant_list"
    template_name = "website/restaurant/restaurant_list.html"

class RestaurantDetail:
    def handle_request(request, pk):
        dishes_from_restaurant = Dish.objects.select_related('restaurant').filter(id=pk)
        context = {"dishes": dishes_from_restaurant}
        return render(request, "website/restaurant/restaurant_detail.html", context=context)
    