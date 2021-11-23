from django.urls import path

from . import studentViews,facultyViews
from . import views
from django.contrib import admin
urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.home, name="home"),
    path('login/',views.loginUser, name = "login"),
    path('loginForm/',views.loginForm, name = "loginForm"),
    path('registration/',views.registration, name = "registration"),
    path('signUp/',views.signUP, name = "signUP"),    
    path('logout_user/', views.logout_user, name="logout_user"),

    #For student portal
    path('student_home/',studentViews.student_home, name = "student_home"),
    path('student_result/',studentViews.student_result, name = "student_result"),
    path('student_attendance/',studentViews.student_attendance, name = "student_attendance"),
    path('view_attendance/',studentViews.view_attendance, name = "view_attendance"),

    #For faculty portal
    path('update_attendance/',facultyViews.update_attendance,name="update_attendance"),
    path('add_result/',facultyViews.add_result,name="add_result"),
    path('take_attendance/',facultyViews.take_attendance,name="take_attendance"),
    path('faculty_home/',facultyViews.faculty_home,name="faculty_home"),
    path('get_students',facultyViews.get_students,name="get_students"),
    path('save_attendance/',facultyViews.save_attendance,name="save_attendance"),
    path('get_attendance_dates/',facultyViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student',facultyViews.get_attendance_student,name="get_attendance_student"),
    path('update_attendance_data/',facultyViews.update_attendance_data,name="update_attendance_data"),
    path('add_result_save/',facultyViews.add_result_save,name="add_result_save")

]