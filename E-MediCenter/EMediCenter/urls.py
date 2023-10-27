from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home_page, name=""),
    path("HomePage/", views.home_page, name="HomePage"),
    path("book_caregiver/", views.book_caregiver_page, name="BookCaregiverPage"),
    path("book_GP/", views.book_GP_page, name="BookGPPage"),
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
    path('paginated_gps/', views.paginated_gps, name='paginated_gps'),
    path('check_email_and_username/', views.check_email_and_username, name='check_email_and_username'),
    path('appointment/', views.appointment, name='appointment'),
    path('get_unavailable_times/<int:caregiver_id>/', views.get_unavailable_times, name='get_unavailable_times'),
    path('success/', views.success, name='success'),
    path('path_to_get_all_orders_view/', views.get_all_orders, name='get_all_orders'),
    path('path_to_get_recent_orders/', views.get_recent_orders, name='get_recent_orders'),
    path('/path_to_get_all_GP_orders_view/', views.get_all_GP_orders, name='get_all_GP_orders'),
    path('path_to_get_recent_GP_orders/', views.get_recent_GP_orders, name='get_recent_GP_orders'),
    path('logout/', views.logout_view, name='logout'),
    path('path_to_get_recent_GP/',views.get_five_GP,name='get_recent_GP'),
    path('path_to_get_all_GP_view/',views.get_all_dockers,name = '/path_to_get_all_GP_view/'),
    path('AddDockerPage',views.admin_add_doctor_dashboard,name='AddDockerPage'),
    path("add-doctor",views.add_doctor,name="add-doctor"),
    path("caregiver_profile",views.caregiver_profile,name="caregiver_profile"),
    path("Edit_Admin/",views.Edit_Admin,name="Edit_Admin"),
    path('admin-profile/', views.Get_Admin, name='Get_Admin'),
    path('caregiber_profile/', views.Edit_Caregiver,name='Edit_caregiver'),
    path('caregiber_profile/', views.Get_Caregiver,name='Get_caregiver'),
    path('get_caregiver_orders/', views.get_caregiver_orders, name='get_caregiver_orders'),
    path('get_caregiver_orders/', views.caregiver_orders, name='get_caregiver_orders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)