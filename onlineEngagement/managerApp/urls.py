from django.urls import path

from . import studentViews
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

]