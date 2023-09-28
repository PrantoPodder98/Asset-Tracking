from django.contrib.auth.models import User
from django.db import models
# from asset_manager.models import UserProfile 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    # Add other user-related fields as needed

    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    position = models.CharField(max_length=100)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='employees')
    # Other fields as needed

    def __str__(self):
        return self.name
        
class Device(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.IntegerField(default=0)  # 0 for unassigned, 1 for assigned
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class DeviceHandover(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    devices = models.ManyToManyField(Device)  # ManyToMany relationship with Device

    # Add any additional fields you may need

    def __str__(self):
        return f"Devices to/from {self.employee} ({self.start_date} - {self.end_date})"

from django.db import models

class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    checked_out_date = models.DateTimeField()
    checked_in_date = models.DateTimeField(null=True, blank=True)
    condition_when_checked_out = models.CharField(max_length=255)
    condition_when_checked_in = models.CharField(max_length=255, null=True, blank=True)
    # status = models.IntegerField(default=0)

class DeviceAssignment(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    device_log = models.ForeignKey(DeviceLog, on_delete=models.SET_NULL, null=True, blank=True)
