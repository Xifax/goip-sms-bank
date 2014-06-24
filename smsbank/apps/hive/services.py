# encoding: utf-8
# Services go here or (in case of MUCH SERVICE) to services/


from smsbank.apps.hive.models import (
    Device,
    Sms
)


def device_exists(ip, port):
    """Check if device exists. Return either device or True."""
    try:
        return Device.objects.get(ip=ip, port=port)
    except Device.DoesNotExist:
        return False


def get_or_create_device(ip, port, status=True):
    """Either get existing or create new device."""
    device = device_exists(ip, port)
    if not device:
        device = Device(ip=ip, port=port, online=status)
        device.save()

    return device


def new_sms(recipient, message):
    """Create new SMS."""
    sms = Sms(recipient=recipient, message=message)
    sms.save()
    return sms
