import random
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
from django.core.validators import validate_email
from django.urls import reverse
import googlemaps
from .models import Caregiver
from django.core.paginator import Paginator
import requests

def is_valid_address(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # 查询参数
    params = {
        "address": address,
        "key": "AIzaSyBlGBJ1MbtPawltq76TsrzHzrFPFi_uMig"
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    # 检查返回的结果是否有地址
    if data['status'] == "OK" and len(data['results']) > 0:
        return True
    return False

def get_place_details(place_id, api_key):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "address_components",
        "key": "AIzaSyBlGBJ1MbtPawltq76TsrzHzrFPFi_uMig"
    }
    
    response = requests.get(base_url, params=params)
    return response.json()

def home_page(request):
    return render(request, 'index.html')
 
def service_information_page(request):
    return render(request, 'ServiceInformation.html')

def caregiver_dashboard(request):
    return render(request, 'CaregiverDashboard.html')


def book_caregiver_page(request):
    caregivers_matched = []
    gmaps = googlemaps.Client(key='AIzaSyBlGBJ1MbtPawltq76TsrzHzrFPFi_uMig')  
    page_number = request.GET.get('page', 1)
    print(request)
    if request.method == "POST":
        
        distance = request.POST.get('distance')
        street = request.POST.get('street')
        suburb = request.POST.get('suburb')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        user_address = f"{street}, {suburb}, {state}, {postcode}"

        caregivers = Caregiver.objects.all()
        for caregiver in caregivers:
            serve_area_address = caregiver.ServiceArea  # 假设ServeArea是一个地址字段
            matrix = gmaps.distance_matrix(user_address, serve_area_address)
            print(matrix)
            if matrix.get("status") == "OK" and matrix.get("rows"):
                row = matrix["rows"][0]
                if row["elements"][0].get("status") == "OK":
                    actual_distance = row["elements"][0]["distance"].get("value", 0)
                    
                    if actual_distance <= float(distance) * 1000:  # 转换为米
                        caregivers_matched.append(caregiver)


        paginator = Paginator(caregivers_matched, 4)  # 每页显示4个匹配的Caregiver
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "base_url": reverse('BookCaregiverPage')
        }
        caregivers_matched_ids = [caregiver.CaregiverID for caregiver in caregivers_matched]
        request.session['caregivers_matched_ids'] = caregivers_matched_ids

        return render(request, 'select.html', context)

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

        try:
            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.")
            
            # Check if the email is in a valid format
            # 若您使用Django自带的validate_email，请确保它已被导入
            # from django.core.validators import validate_email
            validate_email(email)

            # Validate the password using the custom validation function
            # 若您使用Django自带的validate_password，请确保它已被导入
            # from django.contrib.auth.password_validation import validate_password
            validate_password(password)

            user = User.objects.create_user(username=email, email=email, password=password)
            
            # 创建UserProfile
            if is_caregiver == "on":
                is_caregiver_bool = True
            else:
                is_caregiver_bool = False
            
            chosen_number = random.randint(1, 3)
            chosen_avatar = f"avatars/default{chosen_number}.jpeg"

            UserProfile.objects.create(
                user=user,
                avatar=chosen_avatar,
                is_caregiver=is_caregiver_bool,
            )

            # 登录用户并重定向到相应的dashboard
            login(request, user)
            if is_caregiver_bool:
                return HttpResponseRedirect('/caregiver_dashboard/')  
            else:
                return HttpResponseRedirect('/user_dashboard/') 
        except ValidationError as e:
            error_message = str(e)
            
    if request.method == 'GET':
        error_message = ""
    
    # TODO: error_message的处理（如果需要）
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
        return render(request, 'Customer.html')
    
def paginated_caregivers(request):
    page_number = request.GET.get('page', 1)

    caregivers_matched_ids = request.session.get('caregivers_matched_ids', [])
    caregivers_matched = Caregiver.objects.filter(CaregiverID__in=caregivers_matched_ids)

    paginator = Paginator(caregivers_matched, 4)  # 每页显示4个匹配的Caregiver
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }

    return render(request, 'select.html', context)
