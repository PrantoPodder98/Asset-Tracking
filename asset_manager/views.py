# asset_tracking/views.py
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django import forms
    

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Try to retrieve UserProfile associated with the user
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # UserProfile doesn't exist yet, create it
                user_profile = UserProfile.objects.create(user=user, company_name='Default Company Name')

            messages.success(request, 'Login successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if not UserProfile.objects.filter(user=user).exists():
                # Create UserProfile only if it doesn't exist
                UserProfile.objects.create(user=user, company_name='Default Company Name')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration_form.html', {'form': form})

@login_required
def update_company_name(request):
    user_profile = request.user.userprofile  # Assuming the related name is 'userprofile'

    class UserProfileForm(forms.ModelForm):
        class Meta:
            model = UserProfile
            fields = ['company_name']

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard or wherever you want
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'update_company.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'dashboard.html', {'user': user, 'user_profile': user_profile})
