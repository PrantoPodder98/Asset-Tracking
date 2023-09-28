# asset_tracking/views.py

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile, Company
from django.http import HttpResponseBadRequest

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            # Retrieve UserProfile associated with the user
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # Handle the case where UserProfile doesn't exist yet
                pass
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
def create_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        user_profile = UserProfile.objects.get(user=request.user)
        Company.objects.create(user_profile=user_profile, name=company_name)
        return redirect('dashboard')
    return render(request, 'create_company.html')

@login_required
def dashboard(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'dashboard.html', {'user': user, 'user_profile': user_profile})
