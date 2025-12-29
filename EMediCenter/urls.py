from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home_page, name=""),
    path("HomePage/", views.home_page, name="HomePage"),
    path('ask/', views.ask_view, name='ask_view'),  # Add this line
    path("book_caregiver/", views.book_caregiver_page, name="BookCaregiverPage"),
    path("book_GP/", views.book_GP_page, name="BookGPPage"),
    path("caregiver_dashboard/", views.caregiver_dashboard, name="Caregiver"),
    # path("service_information/", views.service_information_page, name="ServiceInformationPage"),
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
    # API endpoints (used by dashboards)
    path('api/orders/caregivers/', views.get_all_orders, name='api_caregiver_orders'),
    path('api/orders/caregivers/recent/', views.get_recent_orders, name='api_recent_caregiver_orders'),
    path('api/orders/gps/', views.get_all_GP_orders, name='api_gp_orders'),
    path('api/orders/gps/recent/', views.get_recent_GP_orders, name='api_recent_gp_orders'),
    path('logout/', views.logout_view, name='logout'),
    path('api/doctors/', views.get_all_doctors, name='api_doctors'),
    path('api/doctors/featured/', views.get_featured_doctors, name='api_featured_doctors'),
    path('admin_doctors/', views.admin_doctors_dashboard, name='admin_doctors'),
    path("add-doctor",views.add_doctor,name="add-doctor"),
    path("admin_profile",views.admin_profile,name="admin_profile"),
    path("caregiver_profile",views.caregiver_profile,name="caregiver_profile"),
    path("customer_profile",views.customer_profile,name="customer_profile"),
    
    path("Edit_Admin/",views.Edit_Admin,name="Edit_Admin"),
    path('admin-profile/', views.Get_Admin, name='Get_Admin'),

    path('Get_caregiver', views.Get_Caregiver,name='Get_caregiver'),
    path("caregiver_profile",views.caregiver_profile,name="caregiver_profile"),

    path('get_caregiver_orders/', views.get_caregiver_orders, name='get_caregiver_orders'),
    path('caregiver_order/', views.caregiver_order, name='caregiver_order'),
    path('caregiver_edit',views.Edit_Caregiver,name = "Edit_caregiver"),
    
    path("doctor_profile_view",views.doctor_profile,name="doctor_profile_view"),
    path('doctor_edit', views.Edit_doctor,name='Edit_doctor'),
    path('doctor_profile', views.Get_doctor,name='Get_doctor'),

    path('customer_profile/', views.Edit_customer,name='Edit_customer'),
    path('get_profile/', views.Get_customer,name='Get_customer'),

    path("customer_order",views.customer_order,name="customer_order"),
    
    path("doctor_order",views.doctor_order,name="doctor_order"),
    path("get_doctor_orders/",views.get_doctor_orders,name="get_doctor_orders"),
    
    # path('get_customer_orders/', views.get_customer_orders, name='get_customer_orders'),
    path("get_user_orders/",views.get_user_orders,name="get_user_orders"),
    path("get_gp_orders/",views.get_gp_orders,name="get_gp_orders"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
