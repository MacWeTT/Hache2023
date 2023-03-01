from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib.auth.decorators import login_required

def Landing(request):
    return render(request, 'landing.html')

def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist.")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exist.")
            
    
    context = {'page': page}
    return render(request, 'login.html',context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def SignUpPage(request):
    form = MyUserCreationForm()
    
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured. Check if passwords match.')
    
    context = {"form":form}
    return render(request, 'signup.html', context)

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def Profile(request):
    return render(request,'profile.html')