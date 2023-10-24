from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home_page, name=""),
    path("HomePage/", views.home_page, name="HomePage"),
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
    path("profile/",views.user_profile,name="profile"),
    path("checkPassword/",views.validate_password,name="checkPassword"),
    path('paginated_caregivers/', views.paginated_caregivers, name='paginated_caregivers'),
    path('check_email_and_username/', views.check_email_and_username, name='check_email_and_username'),
    path("appointment/",views.appointment,name="appointment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)