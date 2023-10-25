import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
import re
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.urls import reverse
import googlemaps
from .models import Caregiver,CaregiverOrder,UserProfile,GPOrder,GP
from django.core.paginator import Paginator
import requests
import datetime
from django.contrib import messages


def is_caregiver_available(caregiver_id, start_time, end_time):
    overlapping_orders = CaregiverOrder.objects.filter(
        CaregiverID=caregiver_id,
        start_time__lt=end_time,
        end_time__gt=start_time
    ).count()

    return overlapping_orders == 0

def is_valid_address(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        "address": address,
        "key": "AIzaSyBlGBJ1MbtPawltq76TsrzHzrFPFi_uMig"
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
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

def book_GP_page(request):
    GPs_matched = []
    gmaps = googlemaps.Client(key='AIzaSyBlGBJ1MbtPawltq76TsrzHzrFPFi_uMig')  
    page_number = request.GET.get('page', 1)
    print(request)
    if request.method == "POST":
        
        distance = request.POST.get('distance')
        street = request.POST.get('street')
        suburb = request.POST.get('suburb')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        cost = request.POST.get('cost')
        date = request.POST.get('date')
        user_address = f"{street}, {suburb}, {state}, {postcode}"

        GPs = GP.objects.all()
        for gp in GPs:
            serve_area_address = gp.ServiceArea  
            matrix = gmaps.distance_matrix(user_address, serve_area_address)
            print(matrix)
            if matrix.get("status") == "OK" and matrix.get("rows"):
                row = matrix["rows"][0]
                if row["elements"][0].get("status") == "OK":
                    actual_distance = row["elements"][0]["distance"].get("value", 0)
                    
                    if actual_distance <= float(distance) * 1000 and gp.Cost<= int(cost):  
                        GPs_matched.append(gp)


        paginator = Paginator(GPs_matched, 4) 
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "date": date,
            "base_url": reverse('BookGPPage')
        }
        GPs_matched_ids = [gp.GPID for gp in GPs_matched]
        request.session['GPs_matched_ids'] = GPs_matched_ids

        return render(request, 'selectGP.html', context)

    return render(request, 'BookGPPage.html')

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
        cost = request.POST.get('cost')
        date = request.POST.get('date')
        user_address = f"{street}, {suburb}, {state}, {postcode}"

        caregivers = Caregiver.objects.all()
        for caregiver in caregivers:
            serve_area_address = caregiver.ServiceArea  
            matrix = gmaps.distance_matrix(user_address, serve_area_address)
            print(matrix)
            if matrix.get("status") == "OK" and matrix.get("rows"):
                row = matrix["rows"][0]
                if row["elements"][0].get("status") == "OK":
                    actual_distance = row["elements"][0]["distance"].get("value", 0)
                    
                    if actual_distance <= float(distance) * 1000 and caregiver.Cost<= int(cost):  
                        caregivers_matched.append(caregiver)


        paginator = Paginator(caregivers_matched, 4) 
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "date": date,
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

def login_view(request):
    error_message = ""
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')
        print(request.POST)
        try:
            user = authenticate(request, username= username, password=password)
            print(user)
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

def is_password(password):
    print(password)
    if len(password) < 8:
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[0-9]', password):
        return False

    return True

def check_email_and_username(request):
    
    email = request.GET.get('email')
    username = request.GET.get('username')
    password = request.GET.get('password')
    message = ""

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        message = "Invalid E-Mail"
        return JsonResponse({"message": message})
    elif User.objects.filter(username=username).exists():
        message = "User name exits"
        return JsonResponse({"message": message})
    elif User.objects.filter(email=email).exists():
        message = "E-Mail already exists"
        return JsonResponse({"message": message})
    elif not is_password(password):
        message = "The password must meet the following criteria:\n\nBe at least 8 characters long.\nContain at least one lowercase letter, one uppercase letter and one number."
    
    return JsonResponse({"message": message})

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

def logout_view(request):
    logout(request)
    return redirect('/')

def SignUp(request):
    error_message = ""

    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password = request.POST.get('pw')
        street = request.POST.get('Street')
        suburb = request.POST.get('Suburb')
        state = request.POST.get('State')
        postcode = request.POST.get('Postcode')
        is_caregiver = request.POST.get('register-as-caregiver')  # checkbox
        try:
            validate_password(password)
        except ValidationError as e:
            error_message = str(e)
            return render(request, 'login.html', {'error_message': error_message})
        try:
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.")

            validate_email(email)
            validate_password(password)

            user = User.objects.create_user(username=username, email=email, password=password)

            chosen_number = random.randint(1, 3)
            chosen_avatar = f"avatars/default{chosen_number}.jpeg"
            address = f"{street}, {suburb}, {state}, {postcode}"
            # Always store address in UserProfile
            UserProfile.objects.create(
                user = user,
                address = address,
                avatar = chosen_avatar
            )

            if is_caregiver == "on":
                # Convert address to a single string for Caregiver's ServiceArea
                
                Caregiver.objects.create(
                    Name=username,
                    ServiceArea=address,
                    # Other fields can be populated as needed or set to some default values
                )

            a = login(request, user)
            print(a)
            if is_caregiver == "on":
                return HttpResponseRedirect('/caregiver_dashboard/')
            else:
                return HttpResponseRedirect('/user_dashboard/')
        except ValidationError as e:
            error_message = str(e)

    if request.method == 'GET':
        error_message = ""

    error_message = error_message[2:-2]
    return render(request, 'login.html', {'error_message': error_message})

def get_all_orders(request):
    caregiver_orders = CaregiverOrder.objects.all().values(
        'start_time', 'end_time', 'Cost', 'CaregiverID__CaregiverID', 'UserID__id'
    )
    data = list(caregiver_orders)
    return JsonResponse(data, safe=False)

def get_recent_GP_orders(request):
    # 获取最新的5个订单
    GP_orders = GPOrder.objects.all().order_by('-start_time')[:5].values(
        'start_time', 'end_time', 'Cost', 'GPID__GPID', 'UserID__id'
    )
    data = list(GP_orders)
    return JsonResponse(data, safe=False)

def get_all_GP_orders(request):
    GP_orders = GPOrder.objects.all().values(
        'start_time', 'end_time', 'Cost', 'GPID__GpID', 'UserID__id'
    )
    data = list(GP_orders)
    return JsonResponse(data, safe=False)

def get_recent_orders(request):
    caregiver_orders = CaregiverOrder.objects.all().order_by('-start_time')[:5].values(
        'start_time', 'end_time', 'Cost', 'CaregiverID__CaregiverID', 'UserID__id'
    )
    data = list(caregiver_orders)
    return JsonResponse(data, safe=False)

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
    date = request.GET.get("date")

    caregivers_matched_ids = request.session.get('caregivers_matched_ids', [])
    caregivers_matched = Caregiver.objects.filter(CaregiverID__in=caregivers_matched_ids)

    paginator = Paginator(caregivers_matched, 4)  # 每页显示4个匹配的Caregiver
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "date":date
    }

    return render(request, 'select.html', context)

def paginated_gps(request):
    page_number = request.GET.get('page', 1)
    date = request.GET.get("date")

    gps_matched_ids = request.session.get('gps_matched_ids', [])
    gps_matched = GP.objects.filter(GPID__in=gps_matched_ids)

    paginator = Paginator(gps_matched, 4)  # 每页显示4个匹配的
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "date":date
    }

    return render(request, 'selectGP.html', context)

def get_unavailable_times(request, caregiver_id):
    """
    Return a list of datetime ranges where the caregiver is not available.
    """
    orders = CaregiverOrder.objects.filter(CaregiverID=caregiver_id)

    unavailable_times = []
    for order in orders:
        start = order.start_time
        end = order.end_time
        # Here you might want to convert these to your desired format
        # or adjust the time zone, if necessary.
        unavailable_times.append({"from": start.strftime('%Y-%m-%d %H:%M'), "to": end.strftime('%Y-%m-%d %H:%M')})

    return JsonResponse({"unavailable_times": unavailable_times})

def appointment(request):
    if request.method == "POST":
        print(request)
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")
        caregiver_id = request.POST.get("caregiver_id")
        cost = request.POST.get("cost")
        date = request.POST.get("selected_date")

        # Combine date and time for start and end
        start_time_str = f"{date} {start_time}"
        end_time_str = f"{date} {end_time}"

        # Parse combined date and time
        start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')

        # Check if the start_time is at least 1 hour before end_time
        if end_time - start_time < datetime.timedelta(hours=1):
            # Use messages to display an error
            messages.error(request, "结束时间应该至少在开始时间之后1小时。")
            return redirect('appointment')  # Assume you want to redirect back to the appointment page

        # Check if caregiver is available
        overlapping_orders = CaregiverOrder.objects.filter(
            CaregiverID=caregiver_id,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_orders.exists():
            # Use messages to display an error
            messages.error(request, "所选时间段内看护者不可用。")
            return redirect('appointment')  # Redirect back to the appointment page

        # Save the order
        order = CaregiverOrder(
            UserID=request.user,  # Assuming the user is logged in
            CaregiverID_id=caregiver_id, 
            start_time=start_time,
            end_time=end_time,
            Cost=cost  
        )
        order.save()

        messages.success(request, "预约成功！")
        return redirect('success')  # Redirect to a success page
    

    return render(request, "select.html")  # Render your template if it's a GET request

def success(request):
    return render(request, "success.html")