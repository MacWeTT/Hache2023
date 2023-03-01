from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/',views.LogoutUser, name = 'logout'),
    path('profile/',views.Profile, name='profile'),
    
    path('',views.Landing, name='landing'),
    path('home',views.HomePage, name="home"),
]
