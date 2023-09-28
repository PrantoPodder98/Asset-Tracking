# asset_tracking/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('update-profile/', views.update_company_name, name='update_company_name'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('employee/add/', views.add_or_update_employee, name='add_employee'),
    path('employee/edit/<int:employee_id>/', views.add_or_update_employee, name='edit_employee'),
    path('devices/', views.device_list, name='device_list'),
    path('device/add/', views.add_or_update_device, name='add_device'),
    path('device/edit/<int:device_id>/', views.add_or_update_device, name='edit_device'),
    path('device-handovers/', views.device_handover_list, name='device_handover_list'),
    path('device-handover/add/', views.add_or_update_device_handover, name='add_device_handover'),
    path('device-handover/<int:handover_id>/', views.add_or_update_device_handover, name='edit_device_handover'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('check-out-device/', views.check_out_device, name='check_out_device'),
    path('check-in-device/<int:assignment_id>/', views.check_in_device, name='check_in_device'),
    # Add more URLs for asset tracking and management as needed
]
