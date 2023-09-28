# asset_manager/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Employee, UserProfile, Device, DeviceHandover, DeviceLog, DeviceAssignment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company_name']

class EmployeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'position']

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'description']

class DeviceHandoverForm(forms.ModelForm):
    class Meta:
        model = DeviceHandover
        fields = ['employee', 'start_date', 'end_date', 'devices']

    devices = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for multiple selection
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(DeviceHandoverForm, self).__init__(*args, **kwargs)
        self.fields['devices'].queryset = Device.objects.all()




