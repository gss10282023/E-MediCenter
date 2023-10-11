from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_caregiver_page, name="home"),  
    path("book_caregiver/", views.book_caregiver_page, name="BookCaregiverPage"),
    path("caregiver_dashboard/", views.caregiver_dashboard, name="Caregiver"),
    path("service_information/", views.service_information_page, name="ServiceInformationPage"),
    path("About/",views.about,name = "AboutusPage"),
    path("Donation/",views.donation,name="Donation"),
    path("Login",views.login_view,name="Login"),
    path("SignUp",views.SignUp,name = "SignUp"),
    path("admin_dashboard/",views.admin_dashboard, name="admin"),
    path("user_dashboard/",views.customer_dashboard, name="customer"),
    path("doctor_dashboard/",views.doctor_dashboard, name="doctor"),
]
