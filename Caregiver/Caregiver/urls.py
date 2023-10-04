from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_caregiver_page, name="home"),  # 添加这一行
    path("book_caregiver/", views.book_caregiver_page, name="BookCaregiverPage"),
    path("caregiver_dashboard/", views.caregiver_dashboard, name="CaregiverDashboard"),
    path("service_information/", views.service_information_page, name="ServiceInformationPage"),
    path("About/",views.about,name = "AboutusPage"),
    path("Donation/",views.donation,name="Donation"),
    path("Login",views.login,name="Login"),
    path("SignUp",views.SignUp,name = "SignUp")
]
