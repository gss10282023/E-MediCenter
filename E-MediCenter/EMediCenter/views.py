from django.http import HttpResponse
from django.shortcuts import render
 
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

def login(request):
    return render(request,'LoginPage.html')

def SignUp(request):
    return render(request,"signup.html")


