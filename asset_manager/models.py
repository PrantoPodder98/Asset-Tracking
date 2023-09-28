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
    status = models.IntegerField(default=0)  # Default status is 0 (not handed over)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# class EmployeeDevice(models.Model):
#     employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
#     device = models.OneToOneField(Device, on_delete=models.CASCADE, unique=True)

#     def __str__(self):
#         return f"{self.employee.name}'s {self.device.name}"

# class DeviceLog(models.Model):
#     device = models.ForeignKey(Device, on_delete=models.CASCADE)
#     checked_out_by = models.ForeignKey(Employee, related_name='checkouts', on_delete=models.CASCADE)
#     checked_in_by = models.ForeignKey(Employee, related_name='checkins', null=True, blank=True, on_delete=models.CASCADE)
#     checkout_time = models.DateTimeField()
#     checkin_time = models.DateTimeField(null=True, blank=True)
#     condition_on_checkout = models.CharField(max_length=100)
#     condition_on_checkin = models.CharField(max_length=100, null=True, blank=True)