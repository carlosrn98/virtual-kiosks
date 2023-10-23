from django.contrib import admin
from django.urls import path, include
from register import views

urlpatterns = [
    path("client/", include("website.urls")),
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout")
]
