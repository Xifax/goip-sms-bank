# coding: utf-8

# Django modules
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import(
    login as login_user,
    logout as logout_user,
    authenticate
)

# Project modules
from forms import (
    SMSForm,
    CustomAuthForm,
    CustomRegisterForm,
    CallForwardingForm
)
from models import (
    DeviceList,
    Device,
    CallForwarding
)
from services import (
    associate_profiles,
    new_call_forwarding_profile,
    sms_list,
    get_device_by_id
)

################
# Landing page #
################


def index(request):
    """Display landing page"""
    if request.user.is_authenticated():
        return redirect('grunts')

    return render(request, 'home.html')


def login(request):
    """Login existing user and redirect to device list page"""

    if request.user.is_authenticated():
        return redirect('grunts')

    if request.method == 'POST':
        form = CustomAuthForm(data=request.POST)
        if not form.is_valid():
            return render(
                request,
                'auth/login.html',
                {'form': form}
            )

        # If form is valid, try to authenticate user
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            # Log in and redirect to device list
            login_user(request, user)
            return redirect('grunts')
        else:
            return render(
                request,
                'auth/login.html',
                {'form': form}
            )
    else:
        form = CustomAuthForm()

    return render(request, 'auth/login.html', {'form': form})


def register(request):
    """Try to register new user"""

    if request.user.is_authenticated():
        return redirect('grunts')

    if request.method == 'POST':
        form = CustomRegisterForm(data=request.POST)
        if not form.is_valid():
            return render(
                request,
                'auth/register.html',
                {'form': form}
            )
        else:
            # If valid form -> create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            # And associate all required profiles
            associate_profiles(user)

            # Login registered user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login_user(request, user)

            # Go to device list
            return redirect('grunts')
    else:
        form = CustomRegisterForm()

    return render(request, 'auth/register.html', {'form': form})

#####################
# Working with hive #
#####################


def grunts(request):
    """Display device list"""

    if not request.user.is_authenticated():
        return redirect('login')

    # Get device list available for this user
    try:
        device_list = request.user.device_list.get()
        devices = device_list.devices.all()

    # If admin, re-scan device list
    except DeviceList.DoesNotExist:
        devices = Device.objects.all()

    return render(
        request,
        'devices/grunts.html',
        {'grunts': devices}
    )


def grunt_list(request, grunt):
    """Display device sms list and controls"""

    if not request.user.is_authenticated():
        return redirect('index')

    device = get_device_by_id(grunt)
    if not device:
        raise Http404

    sms_sent = sms_list(device)

    return render(
        request,
        'devices/grunt.html',
        {'grunt': device, 'sms_sent': sms_sent}
    )


def grunt_send(request, grunt):
    """Send SMS via specified grunt"""

    if not request.user.is_authenticated():
        return redirect('index')

    sms_sent = False
    error_message = False

    if request.method == 'POST':
        form = SMSForm(data=request.POST)
        if form.is_valid():
            sms_sent = True
        else:
            error_message = u'Указаны неверные данные'
    else:
        form = SMSForm()

    return render(request, 'devices/sms-send.html', {
        'grunt': grunt,
        'form': form,
        'sms_sent': sms_sent,
        'error_message': error_message,
    })


def logout(request):
    """Try to logout existing user"""
    if request.user.is_authenticated():
        logout_user(request)
        return redirect('index')


##############
# Additional #
##############

def profile(request):
    """Display configuration associated with user account"""
    if not request.user.is_authenticated():
        return redirect('login')

    profile_updated = False
    error_message = False

    # Get or create profile
    try:
        profile = request.user.call_forwarding.get()
    except CallForwarding.DoesNotExist:
        profile = new_call_forwarding_profile(request.user)

    if request.method == 'POST':
        form = CallForwardingForm(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile_updated = True
        else:
            error_message = u'Не все поля заполнены как надо!'
    else:
        form = CallForwardingForm(instance=profile)

    return render(request, 'profile/main.html', {
        'form': form,
        'profile_updated': profile_updated,
        'error_message': error_message
    })

##############
# Additional #
##############


def info(request):
    """Display application info"""
    return render(request, 'about.html')
