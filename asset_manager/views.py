# asset_tracking/views.py
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile, Employee, Device, DeviceHandover, DeviceLog, DeviceAssignment
from django.http import HttpResponseBadRequest
from django.contrib import messages
from .forms import UserProfileForm, EmployeeRegistrationForm, UserRegistrationForm, DeviceForm, DeviceHandoverForm
from django.shortcuts import get_object_or_404
from django.db import transaction


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

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard or wherever you want
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'update_company.html', {'form': form})

@login_required
def add_or_update_employee(request, employee_id=None):
    if employee_id:
        # Editing an existing employee
        employee = get_object_or_404(Employee, id=employee_id)
        user = employee.user  # Get the associated user
    else:
        # Adding a new employee
        employee = None
        user = None

    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, instance=employee)
        user_form = UserRegistrationForm(request.POST, instance=user)

        if form.is_valid() and user_form.is_valid():
            user = user_form.save()
            if not employee:
                # Creating a new employee
                employee = form.save(commit=False)
            
            # Set the user_profile for the employee
            if request.user.userprofile:
                employee.user_profile = request.user.userprofile
            else:
                # Handle the case where the request user doesn't have a userprofile
                pass

            employee.user = user
            employee.save()
            messages.success(request, 'Employee added/updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeRegistrationForm(instance=employee)
        user_form = UserRegistrationForm(instance=user)

    return render(request, 'employee_form.html', {'form': form, 'user_form': user_form, 'employee': employee})

@login_required
def employee_list(request):
    # Filter employees by the currently logged-in user's ID
    employees = Employee.objects.filter(user_profile=request.user.userprofile)
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def add_or_update_device(request, device_id=None):
    if device_id:
        device = get_object_or_404(Device, id=device_id)
    else:
        device = None

    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device = form.save(commit=False)
            device.user_profile = request.user.userprofile  # Set the user_profile
            device.save()
            messages.success(request, 'Device added/updated successfully.')
            return redirect('device_list')
    else:
        form = DeviceForm(instance=device)

    return render(request, 'device_form.html', {'form': form, 'device': device})


@login_required
def device_list(request):
    devices = Device.objects.filter(user_profile=request.user.userprofile)
    return render(request, 'device_list.html', {'devices': devices})

from django.db import transaction

# ...
@login_required
def add_or_update_device_handover(request, handover_id=None):
    if handover_id:
        handover = get_object_or_404(DeviceHandover, id=handover_id)
    else:
        handover = None

    # Filter employees and devices by the logged-in user's user_profile
    employees = Employee.objects.filter(user_profile=request.user.userprofile)
    devices = Device.objects.filter(user_profile=request.user.userprofile)

    if request.method == 'POST':
        form = DeviceHandoverForm(request.POST, instance=handover)
        if form.is_valid():
            device_handover = form.save(commit=False)
            device_handover.user_profile = request.user.userprofile
            device_handover.save()
            form.save_m2m()  # Save the many-to-many relationships (devices)
            messages.success(request, 'Device Handover added/updated successfully.')
            return redirect('device_handover_list')
    else:
        form = DeviceHandoverForm(instance=handover)

    return render(request, 'device_handover_form.html', {
        'form': form,
        'handover': handover,
        'employees': employees,
        'devices': devices,
    })



@login_required
def device_handover_list(request):
    handovers = DeviceHandover.objects.filter(employee__user_profile=request.user.userprofile)
    return render(request, 'device_handover_list.html', {'handovers': handovers})

@login_required
def dashboard(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'dashboard.html', {'user': user, 'user_profile': user_profile})


# Function to create a new device assignment along with log entry for checking out
def check_out_device(request):
    if request.method == 'POST':
        form = DeviceHandoverForm(request.POST)
        if form.is_valid():
            device_assignment = form.save(commit=False)
            device_assignment.user_profile = request.user.userprofile
            device_assignment.status = 1  # Set status to "Assigned"
            device_assignment.save()

            # Create a corresponding DeviceLog entry for checking out
            device_log = DeviceLog(
                device=device_assignment.device,
                checked_out_date=device_assignment.start_date,
                condition_when_checked_out=device_assignment.condition,
            )
            device_log.save()

            device_assignment.device_log = device_log
            device_assignment.save()

            # Redirect to the device assignment list or device details page
            return redirect('device_assignment_list')
    else:
        form = DeviceHandoverForm(initial={'user_profile': request.user.userprofile})

    return render(request, 'device_handover_form.html', {'form': form})

# Function to update an existing device assignment along with log entry for checking in
def check_in_device(request, assignment_id):
    device_assignment = get_object_or_404(DeviceAssignment, id=assignment_id)

    if request.method == 'POST':
        form = DeviceHandoverForm(request.POST, instance=device_assignment)
        if form.is_valid():
            device_assignment = form.save(commit=False)
            device_assignment.user_profile = request.user.userprofile
            device_assignment.status = 0  # Set status to "Available" upon return
            device_assignment.save()

            # Get the associated DeviceLog entry and update it for checking in
            device_log = device_assignment.device_log
            if device_log:
                device_log.checked_in_date = device_assignment.end_date
                device_log.condition_when_checked_in = device_assignment.condition
                device_log.save()

            # Redirect to the device assignment list or device details page
            return redirect('device_assignment_list')
    else:
        form = DeviceHandoverForm(instance=device_assignment)

    return render(request, 'device_handover_form.html', {'form': form})

