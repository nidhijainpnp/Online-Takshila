from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from .models import *
from django.contrib import messages
import datetime

def student_result(request):
    student = Student.objects.get(userType=request.user.id)
    student_result = Result.objects.filter(student_id=student.id)
    context = {
        "student_result":student_result,
    }
    return render(request, "student/result.html", context)

def student_attendance(request):
    student = Student.objects.get(userType=request.user.id)
    courses = Courses.objects.filter(programId = student.programId)
    context = {
        "courses" : courses
    }
    return render(request,"student/attendance.html", context)

def view_attendance(request):
    course_id = request.POST.get('subject')
    input_start_date = request.POST.get('start_date')
    input_end_date = request.POST.get('end_date')

    course = Courses.objects.get(id = course_id)
    user = CustomUser.objects.get(id = request.user.id)
    student = Student.objects.get(admin = user)

    start_date = datetime.datetime.strptime(input_start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(input_end_date, '%Y-%m-%d').date()

    attendance = Attendance.objects.filter(date__range=(start_date,end_date), course_id=course)
    report = AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=student) 

    context = {
        "course" : course,
        "report" : report
    }
    return render(request, 'attendance_data.html',context)

def student_home(request):
    student = Student.objects.get(admin=request.user.id)
    total_days = AttendanceReport.objects.filter(student_id = student).count()
    total_present = AttendanceReport.objects.filter(student_id = student, is_present=True).count()
    total_absent = AttendanceReport.objects.filter(student_id = student, is_present=False).count()

    program = Program.objects.get(id = student.programId.id)
    registered_courses_count = Courses.objects.filter(programId = program).count()
    registered_courses_data = Courses.objects.filter(programId = student.programId)

    course_name_list = []
    present_list = []
    absent_list = []

    for course in registered_courses_data:
        attendance = Attendance.objects.filter(course_id = course.id)
        count_present = AttendanceReport.objects.filter(attendance_id__in = attendance, is_present = True, student_id = student.id).count()
        count_absent = AttendanceReport.objects.filter(attendance_id__in = attendance, is_present = True, student_id = student.id).count()
        course_name_list.append(course.courseName)
        present_list.append(count_present)
        absent_list.append(count_absent)
        
    context = {
            "total_days": total_days,
            "total_present": total_present,
            "total_absent":total_absent,
            "registered_courses_count":registered_courses_count,
            "course_name_list":course_name_list,
            "present_list":present_list,
            "absent_list":absent_list
        }
    return render(request, "student/home.html",context)

