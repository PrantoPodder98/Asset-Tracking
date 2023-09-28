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
    path('dashboard/', views.dashboard, name='dashboard'),
    # Add more URLs for asset tracking and management as needed
]
