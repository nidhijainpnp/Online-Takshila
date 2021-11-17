from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import *
from django.contrib import messages

def student_result(request):
    student = Student.objects.get(userType=request.user.id)
    student_result = Result.objects.filter(student_id=student.id)
    context = {
        "student_result":student_result,
    }
    return render(request, "student/result.html", context)