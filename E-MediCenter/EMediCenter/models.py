import os
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_doctor = models.BooleanField(default=False)
    is_caregiver = models.BooleanField(default=False)
    height = models.PositiveIntegerField(null=True, blank=True)  # 单位可以是厘米
    weight = models.PositiveIntegerField(null=True, blank=True)  # 单位可以是千克
    gender = models.CharField(max_length=10, null=True, blank=True, choices=[('Male', 'M'), ('Female', 'F'), ('Other', 'O')])
    avatar = models.ImageField(upload_to='avatars/', default='default.jpg')  # 用户头像字段

class GP(models.Model):
    GPID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)
    Gender = models.CharField(max_length=5, null=False)
    Age = models.PositiveSmallIntegerField(null=False)
    Qualification = models.CharField(max_length=100)
    Experience = models.PositiveIntegerField(null=False)
    ServiceArea = models.CharField(max_length=10, null=False)
    Availability = models.CharField(max_length=30, null=False)


class Caregiver(models.Model):
    CaregiverID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)
    Gender = models.CharField(max_length=5, null=False)
    Age = models.PositiveSmallIntegerField(null=False)
    Qualification = models.CharField(max_length=100)
    Experience = models.PositiveIntegerField(null=False)
    ServiceArea = models.CharField(max_length=10, null=False)
    Availability = models.CharField(max_length=30, null=False)
    avatar = models.ImageField(upload_to='avatars/', default='default1.jpg')  # 看护者的头像字段

class CaregiverOrder(models.Model):
    CaregiverOrderID = models.PositiveIntegerField(primary_key=True)
    UserID = models.OneToOneField(User, on_delete=models.CASCADE)
    CaregiverID = models.ForeignKey(Caregiver, on_delete=models.CASCADE) 
    Cost = models.PositiveSmallIntegerField()
    start_time = models.DateTimeField(null=True)  # 开始时间
    end_time = models.DateTimeField(null=True)  # 结束时间

class GPOrder(models.Model):
    GPOrderID = models.PositiveIntegerField(primary_key=True)
    Date = models.DateField(null=False)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    GPID = models.ForeignKey(GP, on_delete=models.CASCADE)
    Cost = models.PositiveSmallIntegerField()

class PatientCase(models.Model):
    case_id = models.AutoField(primary_key=True)  # 病例编号
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')  # 用户编号
    disease_name = models.CharField(max_length=100)  # 病的名字
    symptoms = models.TextField()  # 症状
    diagnosing_doctor = models.ForeignKey(GP, on_delete=models.SET_NULL, null=True, related_name='diagnosed_cases')  # 诊断医生编号
    description = models.TextField()  # 具体描述
    prescription = models.TextField()  # 处方
    diagnosis_date = models.DateField()  # 诊断日期