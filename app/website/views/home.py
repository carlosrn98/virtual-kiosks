import traceback
from django.shortcuts import render

def index(request):
    print(f"{request.user.username} {request.user.groups.all()}")
    try:
        return render(request, "website/index.html")
    except Exception as e:
        print(f"Error: {traceback.print_exception(e)}")