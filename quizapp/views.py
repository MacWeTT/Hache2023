from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def Landing(request):
    return render(request, 'landing.html')

def LoginPage(request):
    return render(request, 'login.html')

@login_required
def HomePage(request):
    return render(request, 'home.html')