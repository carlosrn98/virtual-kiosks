from django.contrib import admin
from django.urls import path, include
from register import views
from django.shortcuts import redirect

urlpatterns = [
    path("client/", include("website.urls")),
    path("", lambda request: redirect("/client", permanent=False)),
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout")
]
