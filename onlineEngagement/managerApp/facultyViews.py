from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login

from .models import *
from django.contrib import messages
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

def faculty_home(request):
    courses = Courses.objects.filter(staffId = request.user.id)
    programIdList = []
    for course in courses:
        programId =  Program.objects.get(id=course.programId.id)
        if programId not in programIdList:
            programIdList.append(programId)
        
    students = Student.objects.filter(programId__in=programIdList)
    students_count = students.count()
    course_count = courses.count()

    #getting attendance count
    attendance_count = Attendance.objects.filter(course_id__in=courses).count()

    #attendance data by courses
    courses_list=[]
    attendance_list=[]
    for course in courses:
        cnt = Attendance.objects.filter(course_id = course.id).count()
        courses_list.append(course.courseName)
        attendance_list.append(cnt)
    
    students_list=[]
    students_present_list=[]
    students_absent_list=[]
    for student in students:
        present_count = AttendanceReport.objects.filter(student_id=student.id,is_present=True).count()
        absent_count = AttendanceReport.objects.filter(student_id=student.id,is_present=False).count()
        students_list.append(student.admin.first_name+" "+student.admin.last_name)
        students_present_list.append(present_count)
        students_absent_list.append(absent_count)
    
    context={
        "students_count":students_count,
        "attendance_count":attendance_count,
        "course_count":course_count,
        "courses_list":courses_list,
        "attendance_list":attendance_list,
        "students_list":students_list,
        "students_present_list":students_present_list,
        "students_absent_list":students_absent_list
    }
    return render(request, "faculty/home.html",context)

def take_attendance(request):
    courses = Courses.objects.filter(staffId = request.user.id)
    return render(request,"faculty/take_attendance.html",{"courses":courses})

def add_result(request):
    courses = Courses.objects.filter(staffId = request.user.id)
    return render(request,"faculty/add_result.html",{"courses":courses})

def add_result_save(request):
    if request.method!="POST":
        messages.error(request,"Invalid!!!!")
        return redirect('add_result')
    else:
        student_list = request.POST.get('student_list')
        exam_marks = request.POST.get('exam_marks')
        course_id = request.POST.get('subject')

        student = Student.objects.get(admin=student_list)
        course = Courses.objects.get(id = course_id)

        try:
            #if result exists update it
            check = Result.objects.filter(course_id=course,student_id = student)
            if check:
                result = Result.objects.get(course_id=course,student_id = student)
                result.course_marks = exam_marks
                result.save()
                messages.success(request,"Success:Updated !!")
                return redirect('add_result')
            else:
                result = Result(student_id = student,course_id = course, course_marks = exam_marks)
                result.save()
                messages.success(request,"Success:Added !!")
                return redirect('add_result')
        except:
            messages.error(request,"Failed to add result!!")
            return redirect('add_result')

@csrf_exempt
def get_students(request):
    input_course = request.POST.get('course')
    course = Courses.objects.get(id = input_course)
    students = Student.objects.filter(programId = course.programId)

    # pass studentid and name
    data_list=[]
    for student in students:
        data = {"id":student.admin.id,
                "name":student.admin.first_name+" "+student.admin.last_name}
        data_list.append(data)
    return JsonResponse(json.dumps(data_list),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance(request):
    # getting values from take_attendance form
    students = request.POST.get("students")
    course_id = request.POST.get("course_id")
    attendance_date = request.POST.get("attendance_date")

    course = Courses.objects.get(id = course_id)
    json_student = json.loads(students)
    try:
        attendance = Attendance(course_id = course,date = attendance_date)
        attendance.save()
        for student in json_student:
            # attendance of individual std from AttendanceReport model
            
            std = Student.objects.get(admin=student['id'])
            attendance_report = AttendanceReport(student_id = std,attendance_id = attendance,is_present = student['is_present'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error!!")

def update_attendance(request):
    courses = Courses.objects.filter(staffId = request.user.id)
    return render(request, "faculty/update_attendance.html",{"courses":courses})

@csrf_exempt
def get_attendance_dates(request):
    #getting values from POST 'Fetch Student'
    course_id = request.POST.get("course_id")
    course = Courses.objects.get(id = course_id)
    attendance = Attendance.objects.filter(course_id=course)

    data_list=[]
    for att in attendance:
        data = {"id":att.id,
                "attendance_date":str(att.date),
                }
        data_list.append(data)
    return JsonResponse(json.dumps(data_list),content_type="application/json",safe=False)

@csrf_exempt
def get_attendance_student(request):
    #getting values from POST 'Fetch Student'
    input_attendanceDate = request.POST.get("input_attendanceDate")
    attendance = Attendance.objects.get(id=input_attendanceDate)

    attendance_report = AttendanceReport.objects.filter(attendance_id = attendance)

    data_list=[]
    for att in attendance_report:
        data = {"id":att.student_id.admin.id,
                "name":att.student_id.admin.first_name+" "+att.student_id.admin.last_name,"is_present":att.is_present
                }
        data_list.append(data)
    return JsonResponse(json.dumps(data_list),content_type="application/json",safe=False)

@csrf_exempt
def update_attendance_data(request):
    # getting values from take_attendance form
    students = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id = attendance_date)

    json_student = json.loads(students)
    
    try:
        for student in json_student:
            # attendance of individual std from AttendanceReport model
            std = Student.objects.get(admin=student['id'])
            attendance_report = AttendanceReport.objects.get(student_id = std,attendance_id = attendance)
            attendance_report.is_present = student['is_present']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error!!")









