import traceback
from django.shortcuts import render

def index(request):
    try:
        return render(request, "website/index.html")
    except Exception as e:
        print(f"Error: {traceback.print_exception(e)}")