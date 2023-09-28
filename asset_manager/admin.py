from django.contrib import admin
from .models import UserProfile, Employee, Device, DeviceHandover, DeviceAssignment, DeviceLog

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Employee)
admin.site.register(Device)
admin.site.register(DeviceHandover)
admin.site.register(DeviceAssignment)
admin.site.register(DeviceLog)

