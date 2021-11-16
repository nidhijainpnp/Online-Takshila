from typing import Text
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
#from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

# sexChoice = (
#     ('Male','Male'),
#     ('Female','Female'),
# )

# programChoice = (
#     ('B.Tech-CSE', 'B.Tech-CSE'),
#     ('B.Tech-Electrical', 'B.Tech-Electrical'),
#     ('B.Tech-Mechanical', 'B.Tech-Mechanical'),
#     ('B.Tech-Civil','B.Tech-Civil'),
# )

# #basketName = 

# class AcademicYear(models.Model):
#     id = models.AutoField(primary_key=True)
#     startYear = models.DateField('Start of Academic Year')
#     EndYear = models.DateField('End of Academic Year')


# adding field of user_type
class CustomUser(AbstractUser):
    userTypeChoices = (
        ('HOD','AdminHOD'),
        ('STAFF','Staff'),
        ('STUDENT','Student'),
    )
    user_type = models.CharField(max_length=7,default='HOD', choices = userTypeChoices)

# # HOD view
# class HOD(models.Model):
#     id = models.AutoField(primary_key=True)
#     userType = models.OneToOneField(CustomerUser, on_delete = models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     lastModified = models.DateTimeField(auto_now=True)

# # Staff View
# class Staff(models.Model):
#     id = models.AutoField(primary_key=True)
#     userType = models.OneToOneField(CustomerUser, on_delete = models.CASCADE)
#     fName = models.CharField(max_length=20)
#     lNmae = models.CharField(max_length=20)
#     gender = models.CharField(choices = sexChoice)
# #    contactNo = PhoneNumberField(unique = True, null = False, blank = False)
#     created = models.DateTimeField(auto_now_add=True)
#     lastModified = models.DateTimeField(auto_now=True)

# # Student View
# class Student(models.Model):
#     id = models.AutoField(primary_key=True)
#     userType = models.OneToOneField(CustomerUser, on_delete = models.CASCADE)
#     fName = models.CharField(max_length=20)
#     lNmae = models.CharField(max_length=20)
#     gender = models.CharField(choices = sexChoice)
#   #  contactNo = PhoneNumberField(unique = True, null = False, blank = False)
#     created = models.DateTimeField(auto_now_add=True)
#     lastModified = models.DateTimeField(auto_now=True)
#     profilePic = models.ImageField()
#     programName = models.CharField(choices=programChoice)

# # BasketOfCourses View
# class BasketOfCourses(models.Model):
#     id = models.AutoField(primary_key=True)
#     basketName = models.CharField(choices=programChoice)

# # Courses View
# class Courses(models.Model):
#     id = models.AutoField(primary_key=True)
#     courseName = models.CharField(max_length=255)
#     programId = models.ForeignKey(BasketOfCourses, on_delete=models.CASCADE)
#     staffId = models.ForeignKey(Staff, on_delete=models.CASCADE)



