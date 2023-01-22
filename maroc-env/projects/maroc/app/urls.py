from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),  
    path('home',views.home,name="home") ,
    path('activate/<uname>',views.activate,name="activate") ,
    path('logout',views.logout,name="logout")  
]