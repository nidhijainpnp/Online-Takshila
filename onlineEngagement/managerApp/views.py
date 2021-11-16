from django.db.models.fields import EmailField
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import *
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'home.html')
 
def loginUser(request):
    return render(request, 'login_page.html')

def registration(request):
    return render(request, 'registration.html')

def contact(request):
    return render(request,'home.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/') 

def loginForm(request):
    emailId = request.GET.get('email')
    password = request.GET.get('password')
    if (not(emailId and password)):
        messages.error(request, "One of the field is empty")
        return render(request, 'login_page.html')

    
    return render(request, 'home.html')

# For initial Purposes only .need to integrate this in login view
def studentPage(request):
    return render(request, 'student/base.html')