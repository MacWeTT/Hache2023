from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('signup/', views.SignUpPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('profile/<str:username>/', views.ViewProfile, name='profile'),
    path('edit-profile/', views.EditProfile, name='editprofile'),
    path('password-change/', views.ChangePasswordView.as_view(),
         name='password_change'),
    path('onboarding/', views.onboardingView, name='onboarding'),

    path('', views.Landing, name='landing'),
    path('home/', views.HomePage, name="home"),
    path('rules/', views.Rules, name='rules'),
    path('hackerboard', views.Hackerboard, name='hackerboard'),

    path('prestart/', views.preStartView, name='prestart'),
    path('quiz/', views.QuizView, name='quiz'),
    path('conclude/', views.conclude, name='conclude'),
    path('winner/', views.WinnerView, name='winner')
]
