from typing import Text
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
 
# #from phonenumber_field.modelfields import PhoneNumberField
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

basketName = (
    ('IC', 'Institute-Core'),
    ('CSE-Dept', 'CSE-Dept'),
    ('Elec-Dept', 'Elec-Dept'),
    ('Mech-Dept', 'Mech-Dept'),
    ('Civil-Dept', 'Civil-Dept'),
    ('HSS Core', 'Humanity Core'),
    ('HSS Elec','Humanity Elective'),
)

class AcademicYear(models.Model):
    id = models.AutoField(primary_key=True)
    startYear = models.DateField('Start of Academic Year')
    EndYear = models.DateField('End of Academic Year')
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)


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
    fName = models.CharField(max_length=20)
    lNmae = models.CharField(max_length=20)
    gender = models.CharField(max_length=10,choices = sexChoice)
#    contactNo = PhoneNumberField(unique = True, null = False, blank = False)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

# Courses View
class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=255)
    staffId = models.ForeignKey(Staff, on_delete=models.CASCADE)
    basketName = models.CharField(max_length=20,choices=basketName)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

# Student View
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    fName = models.CharField(max_length=20)
    lNmae = models.CharField(max_length=20)
    gender = models.CharField(max_length=10,choices = sexChoice)
  #  contactNo = PhoneNumberField(unique = True, null = False, blank = False)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)
    profilePic = models.ImageField(null=True)
    programName = models.CharField(max_length=20,choices=programChoice)
    courseId = models.ForeignKey(Courses, on_delete=models.CASCADE)
    academicYrId = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

# TODO create models for Attendance and Results 
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    date = models.DateField()
    academicYr_id = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    subject_marks = models.FloatField(default=0.0)
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
                                    courseId=Courses.objects.get(id=1),
                                    academicYrId=AcademicYear.objects.get(id=1),
                                    programName="",
                                    profilePic="",
                                    gender="")
     
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "faculty":
        instance.staff.save()
    if instance.user_type == "student":
        instance.student.save()





