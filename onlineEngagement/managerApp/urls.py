from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/',views.loginUser, name = "login"),
    path('loginForm/',views.loginForm, name = "loginForm"),
    path('registration/',views.registration, name = "registration"),
    path('signUp/',views.signUP, name = "signUP"),    
    path('logout_user/', views.logout_user, name="logout"),
    #need to be removed later
    path('student/',views.studentPage, name = "studentPage"),

]