from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, UserProfileForm, UserUpdateForm
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
    
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request,"Sign Up completed successfully.")
            return redirect('home')
        else:
            messages.error(request,'An error occured. Check if passwords match.')
            
    else:
        form = MyUserCreationForm() 
        
    context = {"form":form}
    return render(request, 'signup.html', context)

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def ViewProfile(request,username):
    user = User.objects.get(username=username)  
    profile = Profile.objects.get(user=user)
    context = {'profile':profile}
    return render(request,'profile.html',context)

@login_required(login_url='login')
def EditProfile(request):
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your profile has been updated.')
            return redirect('profile',username=user.username)
    else:
        u_form = UserUpdateForm(instance=request.user) 
        p_form = UserProfileForm(instance=request.user.profile)
        
    context = {'u_form': u_form,'p_form':p_form}
    return render(request, 'editprofile.html',context)