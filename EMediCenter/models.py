import os
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_doctor = models.BooleanField(default=False)
    is_caregiver = models.BooleanField(default=False)
    height = models.PositiveIntegerField(null=True, blank=True)  
    weight = models.PositiveIntegerField(null=True, blank=True)  
    gender = models.CharField(max_length=10, null=True, blank=True, choices=[('Male', 'M'), ('Female', 'F'), ('Other', 'O')])
    avatar = models.ImageField(upload_to='avatars/', default='admin1.png') 
    address = models.CharField(max_length=255, null=True, blank=True)

class GP(models.Model):
    GPID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)
    Gender = models.CharField(max_length=5, null=False)
    Age = models.PositiveSmallIntegerField(null=True)
    Qualification = models.CharField(max_length=100,null=True)
    Experience = models.PositiveIntegerField(null=True)
    ServiceArea = models.CharField(max_length=10, null=False)
    Availability = models.CharField(max_length=30, null=True)
    Cost = models.PositiveSmallIntegerField()
    avatar = models.ImageField(upload_to='avatars/', default='default1.jpg') 


class Caregiver(models.Model):
    CaregiverID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=True)
    Gender = models.CharField(max_length=5, null=True)
    Age = models.PositiveSmallIntegerField(null=True)
    Qualification = models.CharField(max_length=100)
    Experience = models.PositiveIntegerField(null=True)
    ServiceArea = models.CharField(max_length=10, null=False)
    Availability = models.CharField(max_length=30, null=True)
    Cost = models.PositiveSmallIntegerField(null=True)
    avatar = models.ImageField(upload_to='avatars/', default='default1.jpg')  # Caregiver avatar field

class CaregiverOrder(models.Model):
    CaregiverOrderID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CaregiverID = models.ForeignKey(Caregiver, on_delete=models.CASCADE) 
    Cost = models.PositiveSmallIntegerField()
    start_time = models.DateTimeField(null=True)  
    end_time = models.DateTimeField(null=True)  


class GPOrder(models.Model):
    GPOrderID = models.AutoField(primary_key=True)
    Date = models.DateField(null=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    GPID = models.ForeignKey(GP, on_delete=models.CASCADE)
    Cost = models.PositiveSmallIntegerField()
    start_time = models.DateTimeField(null=True)  
    end_time = models.DateTimeField(null=True)  

class PatientCase(models.Model):
    case_id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')  
    disease_name = models.CharField(max_length=100)  
    symptoms = models.TextField()  
    diagnosing_doctor = models.ForeignKey(GP, on_delete=models.SET_NULL, null=True, related_name='diagnosed_cases') 
    description = models.TextField() 
    prescription = models.TextField() 
    diagnosis_date = models.DateField()  
