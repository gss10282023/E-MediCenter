import random
import os
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
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
from django.views.decorators.http import require_http_methods
from .models import CaregiverOrder, Caregiver, GPOrder
from django.views.decorators.http import require_POST
import httpx
import asyncio
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)




def is_caregiver_available(caregiver_id, start_time, end_time):
    overlapping_orders = CaregiverOrder.objects.filter(
        CaregiverID=caregiver_id,
        start_time__lt=end_time,
        end_time__gt=start_time
    ).count()

    return overlapping_orders == 0

def is_valid_address(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    if not api_key:
        return False

    params = {
        "address": address,
        "key": api_key,
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data['status'] == "OK" and len(data['results']) > 0:
        return True
    return False

def get_place_details(place_id, api_key):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    if not api_key:
        raise ValueError("Google Maps API key is not configured.")
    params = {
        "place_id": place_id,
        "fields": "address_components",
        "key": api_key,
    }
    
    response = requests.get(base_url, params=params)
    return response.json()

def home_page(request):
    return render(request, 'index.html')
 
# def service_information_page(request):
#     return render(request, 'ServiceInformation.html')

def caregiver_dashboard(request):
    return render(request, 'caregiver_profile.html')

def book_GP_page(request):
    GPs_matched = []
    google_maps_api_key = getattr(settings, "GOOGLE_MAPS_API_KEY", None)
    gmaps = googlemaps.Client(key=google_maps_api_key) if google_maps_api_key else None
    page_number = request.GET.get('page', 1)
    if not request.user.is_authenticated:
        return render(request, 'login.html')
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
        if not gmaps:
            messages.warning(
                request,
                "Google Maps API key is not configured; distance matching is disabled.",
            )
        for gp in GPs:
            serve_area_address = gp.ServiceArea  
            if not gmaps:
                if gp.Cost <= int(cost):
                    GPs_matched.append(gp)
                continue
            matrix = gmaps.distance_matrix(user_address, serve_area_address)
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
    google_maps_api_key = getattr(settings, "GOOGLE_MAPS_API_KEY", None)
    gmaps = googlemaps.Client(key=google_maps_api_key) if google_maps_api_key else None
    page_number = request.GET.get('page', 1)
    if not request.user.is_authenticated:
        return render(request, 'login.html')
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
        if not gmaps:
            messages.warning(
                request,
                "Google Maps API key is not configured; distance matching is disabled.",
            )
        for caregiver in caregivers:
            serve_area_address = caregiver.ServiceArea  
            if not gmaps:
                if caregiver.Cost <= int(cost):
                    caregivers_matched.append(caregiver)
                continue
            matrix = gmaps.distance_matrix(user_address, serve_area_address)
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
    if not email or not isinstance(email, str) or email.isspace():
        return False
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

# def login_view(request):
#     error_message = ""
#     if request.method == 'POST':
#         username = request.POST.get('Username')
#         password = request.POST.get('password')
#         try:
#             user = authenticate(request, username= username, password=password)
#             if user:
#                 if user.is_active:
#                     login(request, user)
#                     try:
#                         profile = user.userprofile  # Assuming the related name is 'userprofile'
#                         if user.is_staff:
#                             return HttpResponseRedirect('/admin_dashboard/')  # Redirect to the admin's page
#                         elif profile.is_doctor:
#                             return HttpResponseRedirect('/doctor_dashboard/')  # Redirect to the doctor's page
#                         elif profile.is_caregiver:
#                             return HttpResponseRedirect('/caregiver_dashboard/')  
#                         else:
#                             return HttpResponseRedirect('/user_dashboard/')  
#                     except ObjectDoesNotExist:
#                         error_message = "User profile not found."
#                 else:
#                     error_message = "Your account is inactive."
#             else:
#                 error_message = "Invalid login details."
#         except User.DoesNotExist:
#             error_message = "Not a valid email address."
#         except ObjectDoesNotExist:
#             error_message = "Invalid login details."  # Show this when the password is wrong
#     return render(request, 'login.html', {'error_message': error_message})

from django.views.decorators.cache import never_cache
@never_cache
def login_view(request):
    error_message = ""

    if 'error_message' in request.session:
        del request.session['error_message']

    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')
        
        # Check if the user exists first
        try:
            user_instance = User.objects.get(username=username)
        except User.DoesNotExist:
            error_message = "User doesn't exist."
            return render(request, 'login.html', {'error_message': error_message})

        # Check if user is active
        if not user_instance.is_active:
            error_message = "Your account is inactive."
            return render(request, 'login.html', {'error_message': error_message})

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
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
            error_message = "Incorrect password."

    return render(request, 'login.html', {'error_message': error_message})



def is_password(password):
    if len(password) < 8:
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[0-9]', password):
        return False

    return True


def add_doctor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        cost = request.POST.get('cost')
        email = request.POST.get('email')
        street = request.POST.get('street')
        suburb = request.POST.get('suburb')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        
        chosen_number = random.randint(1, 2)
        chosen_avatar = f"avatars/admin{chosen_number}.png"
        address = f"{street}, {suburb}, {state}, {postcode}"

        user = User.objects.create_user(username = name, email=email, password=email)

        UserProfile.objects.create(
            user = user,
            address = address,
            avatar = chosen_avatar,
            is_doctor = 1
        )

        doctor = GP(
            Name=name,
            Gender=gender,
            Cost=cost,
            ServiceArea = address 
        )
        doctor.save()

        return JsonResponse({"message": "Doctor added successfully!"})


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
    if password != None: 
        if  len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")


def logout_view(request):
    logout(request)
    return redirect('/')

def SignUp(request):
    error_message = ""

    if request.method == 'POST':
        username = request.POST.get('Username2')
        email = request.POST.get('Email')
        password = request.POST.get('pw')
        street = request.POST.get('Street')
        suburb = request.POST.get('Suburb')
        state = request.POST.get('State')
        postcode = request.POST.get('Postcode')
        is_caregiver_text = request.POST.get('register-as-caregiver')
        is_caregiver = False
        if(is_caregiver_text == "on"):
            is_caregiver = True
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

            user = User.objects.create_user(username = username, email=email, password=password)

            chosen_number = random.randint(1, 3)
            chosen_avatar = f"avatars/default{chosen_number}.jpeg"
            address = f"{street}, {suburb}, {state}, {postcode}"
            # Always store address in UserProfile
            UserProfile.objects.create(
                user = user,
                address = address,
                avatar = chosen_avatar,
                is_caregiver = is_caregiver
            )

            if is_caregiver == "on":
                # Convert address to a single string for Caregiver's ServiceArea
                

                Caregiver.objects.create(
                    Name=username,
                    ServiceArea=address,
                    Cost = 20,
                )
            login(request, user)
            if is_caregiver:
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

def get_all_doctors(request):
    try:
        doctors_data = GP.objects.all().values(
            'GPID', 'Name', 'Gender', 'Age', 'Qualification','Experience', 'ServiceArea', 'Availability', 'Cost', 'avatar'
        )
        data = list(doctors_data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_featured_doctors(request):
    doctors_data = GP.objects.all().order_by('GPID')[:5].values(
            'GPID', 'Name', 'Gender', 'Age', 'Qualification','Experience', 'ServiceArea', 'Availability', 'Cost', 'avatar'
        )
    data = list(doctors_data)
    return JsonResponse(data, safe=False)


def get_recent_GP_orders(request):
    GP_orders = GPOrder.objects.all().order_by('-start_time')[:5].values(
        'start_time', 'end_time', 'Cost', 'GPID__GPID', 'UserID__id'
    )
    data = list(GP_orders)
    return JsonResponse(data, safe=False)

def get_all_GP_orders(request):
    GP_orders = GPOrder.objects.all().values(
        'start_time', 'end_time', 'Cost', 'GPID__GPID', 'UserID__id'
    )
    data = list(GP_orders)
    return JsonResponse(data, safe=False)

def get_recent_orders(request):
    caregiver_orders = CaregiverOrder.objects.all().order_by('-start_time')[:5].values(
        'start_time', 'end_time', 'Cost', 'CaregiverID__CaregiverID', 'UserID__id'
    )
    data = list(caregiver_orders)
    return JsonResponse(data, safe=False)
def admin_doctors_dashboard(request):
    return render(request, "Dashboard_Admin_doctors.html")


def admin_dashboard(request):
    return render(request,"Dashboard_Admin.html")

def customer_dashboard(request):
    return render(request,"customer_profile.html")

def customer_order(request):
    return render(request,"customer_order.html")

def doctor_dashboard(request):
    return render(request,"doctor_profile.html")

def doctor_order(request):
    return render(request,"doctor_order.html")


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('/Login/')
    if request.user.userprofile.is_doctor:
        return redirect('/doctor_dashboard/')
    elif request.user.userprofile.is_caregiver:
        return redirect('/caregiver_dashboard/')
    elif request.user.is_staff:
        return redirect('/admin_dashboard/')
    else:
        return render(request, 'customer_profile.html')

def paginated_caregivers(request):
    page_number = request.GET.get('page', 1)
    date = request.GET.get("date")

    caregivers_matched_ids = request.session.get('caregivers_matched_ids', [])
    caregivers_matched = Caregiver.objects.filter(CaregiverID__in=caregivers_matched_ids)

    paginator = Paginator(caregivers_matched, 4)  
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

    paginator = Paginator(gps_matched, 4)  
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
            messages.error(request, "The appointment must last at least 1 hour!")
            return redirect('appointment')  # Assume you want to redirect back to the appointment page

        # Check if caregiver is available
        overlapping_orders = CaregiverOrder.objects.filter(
            CaregiverID=caregiver_id,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_orders.exists():
            # Use messages to display an error
            messages.error(request, "Not an available user")
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

        messages.success(request, "Success")
        return redirect('success')  # Redirect to a success page
    

    return render(request, "select.html")  # Render your template if it's a GET request

def success(request):
    return render(request, "success.html")

def admin_profile(request):
    return render(request,"Dashboard_Admin_profile.html")

def caregiver_profile(request):
    return render(request,"caregiver_profile.html")

def caregiver_order(request):
    return render(request,"caregiver_order.html")

def customer_profile(request):
    return render(request,"customer_profile.html")

def customer_order(request):
    return render(request,"customer_order.html")



def doctor_profile(request):
    return render(request,"doctor_profile.html")

def Edit_Admin(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        street = request.POST['street']
        suburb = request.POST['suburb']
        state = request.POST['state']
        postcode = request.POST['postcode']
    
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile = user.userprofile
        profile.address = f"{street}, {suburb}, {state}, {postcode}"  
        profile.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return render(request,"Dashboard_Admin_profile.html")

def get_customer_orders(request):
    return render(request,"customer_order.html")

def Get_Admin(request):
    if request.method == 'GET':
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        user_profile = UserProfile.objects.get(user=request.user)
        address = user_profile.address
        if address:
            parts = address.split(", ")
            if len(parts) == 4:
                street, suburb, state, postcode = parts
        context = {
            'first_name': first_name,
            'last_name':last_name,
            'email':email,
            'street': street,
            'suburb': suburb,
            'state': state,
            'postcode': postcode,
        }
        return render(request, 'Dashboard_Admin_profile.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def get_caregiver_orders(request):
    user_id = request.user.id

    # Fetch the caregiver object associated with the user_id
    try:
        caregiver = Caregiver.objects.get(CaregiverID=user_id)
    except Caregiver.DoesNotExist:
        logger.info("No caregiver found for ID: %s", user_id)
        return JsonResponse([], safe=False)

    caregiver_orders = CaregiverOrder.objects.filter(CaregiverID=caregiver)

    orders_data = []
    for order in caregiver_orders:
        user = order.UserID
        orders_data.append({
            'start_time': order.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': order.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'cost': order.Cost,
            'caregiver_id': caregiver.CaregiverID,
            'user_id': user.id if user else '',
        })

    return JsonResponse(orders_data, safe=False)




@require_http_methods(["GET"])
def get_user_orders(request):
    user_id = request.user.id

    # Fetch the orders associated with this user
    user_orders = CaregiverOrder.objects.filter(UserID=user_id)

    orders_data = []
    for order in user_orders:
        caregiver = order.CaregiverID
        orders_data.append({
            'start_time': order.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': order.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'cost': order.Cost,
            'caregiver_id': caregiver.CaregiverID,
            'user_id': user_id,
        })

    return JsonResponse(orders_data, safe=False)

@require_http_methods(["GET"])
def get_gp_orders(request):
    user_id = request.user.id

    # Fetch the orders associated with this user
    user_orders = GPOrder.objects.filter(UserID=user_id)

    orders_data = []
    for order in user_orders:
        gp = order.GPID
        orders_data.append({
            'start_time': order.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': order.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'cost': order.Cost,
            'gp_id': gp.GPID if gp else '',
            'user_id': user_id,
        })

    return JsonResponse(orders_data, safe=False)

@require_http_methods(["GET"])
def get_doctor_orders(request):
    user_id = request.user.id

    # Fetch the caregiver object associated with the user_id
    try:
        doctor = GP.objects.get(GPID=user_id)
    except GP.DoesNotExist:
        logger.info("No doctor found for ID: %s", user_id)
        return JsonResponse([], safe=False)

    gp_orders = GPOrder.objects.filter(GPID=doctor)

    orders_data = []
    for order in gp_orders:
        user = order.UserID
        orders_data.append({
            'date': order.Date.strftime('%Y-%m-%d'),  # Formatting the date
            'cost': order.Cost,
            'gp_id': doctor.GPID,
            'user_id': user.id if user else '',
    })

    return JsonResponse(orders_data, safe=False)

def Edit_customer(request):

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        street = request.POST.get('street')
        suburb = request.POST.get('suburb')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        cost = request.POST.get('cost')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile = user.userprofile
        profile.address = f"{street}, {suburb}, {state}, {postcode}"  
        profile.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return render(request, "customer_profile.html")

    # If it's a GET request, you can render the edit form here (if you have one)
    else:
        context = {
            'user': request.user,
            # Add other context variables if needed
        }
        return render(request, 'customer_profile.html', context)

def Get_customer(request):
    if request.method == 'GET':
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            address = user_profile.address
        except UserProfile.DoesNotExist:
            return HttpResponseBadRequest("UserProfile does not exist for the user.")
        
        street, suburb, state, postcode = ("", "", "", "")
        if address:
            parts = address.split(", ")
            if len(parts) == 4:
                street, suburb, state, postcode = parts

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'street': street,
            'suburb': suburb,
            'state': state,
            'postcode': postcode,
        }
        return render(request, 'customer_profile.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")

    
def Edit_doctor(request):

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        street = request.POST.get('street')
        suburb = request.POST.get('suburb')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        cost = request.POST.get('cost')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()  # Move user.save() here

        profile = user.userprofile
        profile.address = f"{street}, {suburb}, {state}, {postcode}"  
        profile.save()  # Move profile.save() here

        # Update doctor's Cost
        try:
            doctor = GP.objects.get(Name=user.username)  # Fetching doctor by username
            if cost:
                doctor.Cost = int(cost)  # Convert string to integer
                doctor.save()
        except GP.DoesNotExist:  # Adjust this to GP.DoesNotExist
            pass  # Handle the exception, maybe log an error or send a message to the user

        messages.success(request, 'Your profile has been updated successfully!')
        return render(request, "doctor_profile.html")

    # If it's a GET request, you can render the edit form here (if you have one)
    else:
        context = {
            'user': request.user,
            # Add other context variables if needed
        }
        return render(request, 'doctor_profile.html', context)


def Get_doctor(request):
    if request.method == 'GET':
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            address = user_profile.address
        except UserProfile.DoesNotExist:
            return HttpResponseBadRequest("UserProfile does not exist for the user.")
        
        street, suburb, state, postcode = ("", "", "", "")
        if address:
            parts = address.split(", ")
            if len(parts) == 4:
                street, suburb, state, postcode = parts

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'street': street,
            'suburb': suburb,
            'state': state,
            'postcode': postcode,
        }
        return render(request, 'doctor_profile.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")

def Edit_Caregiver(request):

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        street = request.POST.get('street')
        suburb = request.POST.get('suburb')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        cost = request.POST.get('cost')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()  # Move user.save() here

        profile = user.userprofile
        profile.address = f"{street}, {suburb}, {state}, {postcode}"  
        profile.save()  # Move profile.save() here

        # Update Caregiver's Cost
        try:
            caregiver = Caregiver.objects.get(Name=user.username)  # Fetching Caregiver by username
            if cost:
                caregiver.Cost = int(cost)  # Convert string to integer
                caregiver.save()
        except Caregiver.DoesNotExist:  # Adjust this to Caregiver.DoesNotExist
            pass  # Handle the exception, maybe log an error or send a message to the user

        messages.success(request, 'Your profile has been updated successfully!')
        return render(request, "caregiver_profile.html")

    # If it's a GET request, you can render the edit form here (if you have one)
    else:
        context = {
            'user': request.user,
            # Add other context variables if needed
        }
        return render(request, 'caregiver_profile.html', context)


def Get_Caregiver(request):
    if request.method == 'GET':
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            address = user_profile.address
        except UserProfile.DoesNotExist:
            return HttpResponseBadRequest("UserProfile does not exist for the user.")
        
        street, suburb, state, postcode = ("", "", "", "")
        if address:
            parts = address.split(", ")
            if len(parts) == 4:
                street, suburb, state, postcode = parts

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'street': street,
            'suburb': suburb,
            'state': state,
            'postcode': postcode,
        }
        return render(request, 'caregiver_profile.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method.")


async def get_bot_reply(user_message):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "OpenAI API key is not configured."
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": user_message}],
        "model": "gpt-4",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:  # 30s timeout
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",  # Use the chat/completions endpoint
                headers=headers,
                json=data
            )
    except httpx.ReadTimeout:
        logger.warning("OpenAI request timed out")
        return "Sorry, the request timed out, please send again"  # Return timeout message

    response_data = response.json()

    if 'choices' in response_data:
        return response_data["choices"][0]["message"]["content"].strip()  # Extract chat completion content
    else:
        logger.error("OpenAI API error: %s", response_data.get("error", "Unknown error"))
        return "Sorry, I encountered an error."

@require_POST
@async_to_sync
async def ask_view(request):
    user_message = request.POST.get('user_message')
    bot_reply = await get_bot_reply(user_message)
    return JsonResponse({'bot_reply': bot_reply})
