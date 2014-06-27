# encoding: utf-8
# Services go here or (in case of MUCH SERVICE) to services/


from smsbank.apps.hive.models import (
    Device,
    Sms,
    DeviceList,
    CallForwarding
)

########################
# Working with Devices #
########################


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


def new_sms(recipient, message, device=None):
    """Create new SMS."""
    sms = Sms(recipient=recipient, message=message)
    if device:
        sms.device = device
    sms.save()

    return sms


def sms_list(device):
    """Get SMS sent from the device"""
    return Sms.objects.filter(device=device)


def get_device_by_id(device_id):
    """Get device by id"""
    try:
        return Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return None


#########################
# Working with profiles #
#########################

def associate_profiles(user):
    """Create default profiles for new user"""
    # Associate device list
    profile = DeviceList()
    profile.user = user
    profile.save()

    # Also add forwarding profile
    new_call_forwarding_profile(user)

    return user


def new_call_forwarding_profile(user):
    """Associate new call forwarding profile with user"""
    forwarding = CallForwarding()
    forwarding.user = user
    forwarding.save()

    return forwarding
