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

# class Company(models.Model):
#     user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=100)
    # Add other company-related fields as needed
