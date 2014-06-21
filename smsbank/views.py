from django.shortcuts import redirect


def landing(request):
    """Redirect to HIVE application"""
    return redirect('hive/')
