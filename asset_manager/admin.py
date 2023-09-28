from django.contrib import admin
from .models import UserProfile, Company

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Company)
# admin.site.register(Employee)
# admin.site.register(Device)
# admin.site.register(DeviceLog)

