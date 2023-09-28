# asset_tracking/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('create-company/', views.create_company, name='create_company'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Add more URLs for asset tracking and management as needed
]
