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
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist
import re
from django.core.exceptions import ValidationError


 
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

# def login_view(request):
#     error_message = ""
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         if not is_valid_email(email):
#             error_message = "Not a valid email address."
#         else:
#             checkuser = User.objects.get(email=email)
#             user = authenticate(request, username=checkuser.username, password=password)
            
#             if user:
                
#                 if user.is_active:
#                     login(request, user)
#                     try:
#                         profile = user.userprofile  # Assuming the related name is 'userprofile'
#                         if user.is_staff:
#                             return HttpResponseRedirect('/admin_dashboard/')  # 重定向到管理员的页面
#                         elif profile.is_doctor:
#                             return HttpResponseRedirect('/doctor_dashboard/')  # 重定向到医生的页面
#                         elif profile.is_caregiver:
#                             return HttpResponseRedirect('/caregiver_dashboard/')  
#                         else:
#                             return HttpResponseRedirect('/user_dashboard/')  
#                     except:
#                         error_message = "User profile not found."
#                 else:
#                     error_message = "Your account is inactive."
#             else:
#                 error_message = "Invalid login details." 
#     return render(request, 'login.html', {'error_message': error_message})



def login_view(request):
    error_message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            checkuser = User.objects.get(email=email)
            user = authenticate(request, username=checkuser.username, password=password)
            
            if user:
                if user.is_active:
                    login(request, user)
                    try:
                        profile = user.userprofile  # Assuming the related name is 'userprofile'
                        if user.is_staff:
                            return HttpResponseRedirect('/admin_dashboard/')  # Redirect to the admin's page
                        elif profile.is_doctor:
                            return HttpResponseRedirect('/doctor_dashboard/')  # Redirect to the doctor's page
                        elif profile.is_caregiver:
                            return HttpResponseRedirect('/caregiver_dashboard/')  
                        else:
                            return HttpResponseRedirect('/user_dashboard/')  
                    except ObjectDoesNotExist:
                        error_message = "User profile not found."
                else:
                    error_message = "Your account is inactive."
            else:
                error_message = "Invalid login details."
        except User.DoesNotExist:
            error_message = "Not a valid email address."
        except ObjectDoesNotExist:
            error_message = "Invalid login details."  # Show this when the password is wrong
    return render(request, 'login.html', {'error_message': error_message})


def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one number.")

def is_valid_email(email):
    # Regular expression for a basic email format check
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

def SignUp(request):
    error_message = ""
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_caregiver = request.POST.get('remember-me')  # checkbox  
        print(is_caregiver)

        try:
            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.")
            
            # Check if the email is in a valid format
            if not is_valid_email(email):
                raise ValidationError("Invalid email format.")

            # Validate the password using the custom validation function
            validate_password(password)

            user = User.objects.create_user(email, email, password)
            # UserProfile.objects.create(user=user)
            user_profile = UserProfile(user=user)
            if(is_caregiver == "on"):
                user_profile.is_caregiver = 1
            else:
                user_profile.is_caregiver = 0
            
            user_profile.save()
            user.save()
            
            # # Login the user automatically
            # login(request, user)
            
            # Redirect to the desired dashboard page
            if user.userprofile.is_caregiver:
                return HttpResponseRedirect('/caregiver_dashboard/')  
            else:
                return HttpResponseRedirect('/user_dashboard/') 
            # return redirect('Login')
        except ValidationError as e:
            error_message = str(e)
            
    if request.method == 'GET':
        error_message = ""
    #TODO:
    error_message = error_message[2:-2]
    return render(request, 'signup.html', {'error_message': error_message})


def admin_dashboard(request):
    return render(request,"Dashboard_Admin.html")

def customer_dashboard(request):
    return render(request,"Customer.html")

def doctor_dashboard(request):
    return render(request,"doctor_dashboard.html")

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('Login')

    if request.user.userprofile.is_doctor:
        return redirect('doctor_dashboard')
    elif request.user.userprofile.is_caregiver:
        return redirect('caregiver_dashboard')
    elif request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return render(request, 'regular_user_dashboard.html')