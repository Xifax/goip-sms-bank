from django.contrib import admin
from models import (
    Device,
    DeviceList,
    CallForwarding,
    Sms
)

admin.site.register([Device, Sms, DeviceList, CallForwarding])
