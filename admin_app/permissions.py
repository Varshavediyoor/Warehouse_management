from django.shortcuts import redirect
from django.contrib import messages
from admin_app.models import RoleFunction,UserProfile
def require_function(function_name):
    """
    Decorator to restrict view access based on role-function mapping.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            # if user is not logged in
            if not request.user.is_authenticated:
                messages.error(request, "Please login first.")
                return redirect("user_login")

            # get user role
            try:
                role = request.user.userprofile.role
            except:
                messages.error(request, "Access denied. You do not have permission.")
                return redirect("user_login")

            # get assigned functions for that role
            try:
                role_obj = RoleFunction.objects.get(role=role)
                assigned_functions = role_obj.functions.values_list("name", flat=True)
            except RoleFunction.DoesNotExist:
                assigned_functions = []

            # check permission
            if function_name not in assigned_functions:
                messages.error(request, "Access denied. You do not have permission.")
                return redirect("user_login")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login

def role_required(role_code):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            # simple fallback: allow staff/superuser (replace with your real role logic)
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            # otherwise 403 (you can redirect to a 'no permission' page)
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped
    return decorator

