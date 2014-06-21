from django.contrib import admin
from models import (
    Device,
    DeviceList
)

admin.site.register([Device, DeviceList])
