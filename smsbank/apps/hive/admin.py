from django.contrib import admin
from models import (
    Device,
    DeviceList,
    Sms
)

admin.site.register([Device, DeviceList, Sms])
