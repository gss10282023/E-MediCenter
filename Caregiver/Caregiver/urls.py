from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_caregiver_page, name="home"),  # 添加这一行
    path("book_caregiver/", views.book_caregiver_page, name="BookCaregiverPage"),
    path("caregiver_dashboard/", views.caregiver_dashboard, name="CaregiverDashboard"),
    path("service_information/", views.service_information_page, name="ServiceInformationPage")
]
