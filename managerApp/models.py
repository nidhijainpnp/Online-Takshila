from typing import Text
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
 

# # Create your models here.

sexChoice = (
    ('Male','Male'),
    ('Female','Female'),
)

programChoice = (
    ('B.Tech-CSE', 'B.Tech-CSE'),
    ('B.Tech-Electrical', 'B.Tech-Electrical'),
    ('B.Tech-Mechanical', 'B.Tech-Mechanical'),
    ('B.Tech-Civil','B.Tech-Civil'),
)



# adding field of user_type
class CustomUser(AbstractUser):
    userTypeChoices = (
        ('HOD','AdminHOD'),
        ('faculty','faculty'),
        ('student','student'),
    )
    user_type = models.CharField(max_length=7,default='student', choices = userTypeChoices)

# HOD view
class HOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

# Staff View
class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    # gender = models.CharField(max_length=10,choices = sexChoice)
#    contactNo = PhoneNumberField(unique = True, null = False, blank = False)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)


# Courses View
class Program(models.Model):
    id = models.AutoField(primary_key=True)
    programName = models.CharField(max_length=50,choices=programChoice)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=255)
    programId = models.ForeignKey(Program,on_delete=models.CASCADE, default=1)
    staffId = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

# Student View
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=10,choices = sexChoice)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)
    profilePic = models.ImageField(null=True)
    programId = models.ForeignKey(Program, on_delete=models.DO_NOTHING, default=1)
    

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    course_marks = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

#Creating Django Signals
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "faculty":
            Staff.objects.create(admin=instance)
        if instance.user_type == "student":
            Student.objects.create(admin=instance,
                                    programId=Program.objects.get(id=1),
                                    profilePic="",
                                    gender="")
     
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "faculty":
        instance.staff.save()
    if instance.user_type == "student":
        instance.student.save()





