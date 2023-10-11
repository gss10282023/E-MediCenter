from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import re
from .models import UserProfile

 
def service_information_page(request):
    return render(request, 'ServiceInformation.html')

def caregiver_dashboard(request):
    return render(request, 'CaregiverDashboard.html')

def book_caregiver_page(request):
    return render(request, 'BookCaregiverPage.html')

def about(request):
    return render(request,'AboutusPage.html')

def donation(request):
    return render(request,'DonationPage.html')

def is_valid_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None

def login_view(request):
    error_message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not is_valid_email(email):
            error_message = "Not a valid email address."
        else:
            checkuser = User.objects.get(email=email)
            user = authenticate(request, username=checkuser.username, password=password)
            
            if user:
                
                if user.is_active:
                    login(request, user)
                    
                    profile = user.userprofile  # Assuming the related name is 'userprofile'

                    if user.is_staff:
                        return HttpResponseRedirect('/admin_dashboard/')  # 重定向到管理员的页面
                    elif profile.is_doctor:
                        return HttpResponseRedirect('/doctor_dashboard/')  # 重定向到医生的页面
                    elif profile.is_caregiver:
                        return HttpResponseRedirect('/caregiver_dashboard/')  
                    else:
                        return HttpResponseRedirect('/user_dashboard/')  
                        error_message = "User profile not found."
                else:
                    error_message = "Your account is inactive."
            else:
                error_message = "Invalid login details." 
    return render(request, 'login.html', {'error_message': error_message})


def SignUp(request):
    return render(request,"signup.html")

def admin_dashboard(request):
    return render(request,"Dashboard_Admin.html")

def customer_dashboard(request):
    return render(request,"Customer.html")

def doctor_dashboard(request):
    return render(request,"doctor_dashboard.html")