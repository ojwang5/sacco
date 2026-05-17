from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Member

def get_user_role(user):
    """Get the role of the authenticated user"""
    if not user.is_authenticated:
        return None
    try:
        member = Member.objects.get(user=user)
        return member.role
    except Member.DoesNotExist:
        return None

def user_required(view_func):
    """Decorator for views that require user role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('sacco:login')

        user_role = get_user_role(request.user)
        if user_role not in ['user', 'admin', 'superadmin']:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('sacco:dashboard')

        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    """Decorator for views that require admin or superadmin role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('sacco:login')

        user_role = get_user_role(request.user)
        if user_role not in ['admin', 'superadmin']:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('sacco:dashboard')

        return view_func(request, *args, **kwargs)
    return wrapper

def superadmin_required(view_func):
    """Decorator for views that require superadmin role only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('sacco:login')

        user_role = get_user_role(request.user)
        if user_role != 'superadmin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('sacco:dashboard')

        return view_func(request, *args, **kwargs)
    return wrapper
