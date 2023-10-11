from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. This is index!")

def menu(request):
    return HttpResponse("Este es el menu")
