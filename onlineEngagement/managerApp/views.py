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

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/') 

def loginForm(request):
    emailId = request.GET.get('email')
    password = request.GET.get('password')
    if (not(emailId and password)):
        messages.error(request, "One of the field is empty")
        return render(request, 'login_page.html')
    user = CustomUser.objects.filter(email=emailId, password=password).first()
    if not user:
        user.error(request, "INVALID")
        return render(request,'login_page.html')
    
    login(request, user)
    if(user.user_type == "student"):
        return redirect('../student_home/')
    elif(user.user_type == "faculty"):
        return redirect('../student/')
    
    return render(request, 'home.html')

def signUP(request):
    category = request.GET.get('category')
    fname = request.GET.get('fname')
    lname = request.GET.get('lname')
    email = request.GET.get('email')
    password = request.GET.get('password')
    confirmPassword = request.GET.get('confirmPassword')
    if not (category and fname and email and password and confirmPassword):
        messages.error(request, 'One or many fields is left empty')
        return render(request, 'registration.html')
    
    if( password != confirmPassword):
        messages.error('Passwords do not match')
        return render(request, 'registration.html')

    user = CustomUser()
    user.username = email.split('@')[0]
    user.email = email
    user.password = password
    user.user_type = category
    user.first_name = fname
    user.last_name = lname
    user.save()
    # print(user.user_type+"\n\n\n")
    # if category == "student" :
    #     Student.objects.create(admin =user)
    # elif category== "faculty":
    #     Staff.objects.create(admin = user)
    return render(request, 'login_page.html')


    

# For initial Purposes only .need to integrate this in login view
def studentPage(request):
    return render(request, 'student/base.html')