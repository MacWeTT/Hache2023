from django.urls import path
from . import views

urlpatterns = [
    path('',views.Landing, name='landing'),
    path('home',views.HomePage, name="home"),
]
