# from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=100)
