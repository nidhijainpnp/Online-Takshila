from django.urls import path

from . import studentViews
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/',views.loginUser, name = "login"),
    path('loginForm/',views.loginForm, name = "loginForm"),
    path('registration/',views.registration, name = "registration"),
    path('signUp/',views.signUP, name = "signUP"),    
    path('logout_user/', views.logout_user, name="logout"),
    #need to be removed later
    path('student_home/',studentViews.student_home, name = "studentPage"),

]