from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import UserRole


def login_view(request):
    """Unified login for both Admin and Employee roles."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Remember me — extend session
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)

            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm(request)

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """Log out the user and redirect to login."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


def forgot_password_view(request):
    """Forgot password — UI only placeholder."""
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email:
            messages.success(
                request,
                f'If {email} is registered, a password reset link has been sent.'
            )
            return redirect('login')
        else:
            messages.error(request, 'Please enter a valid email address.')

    return render(request, 'auth/forgot_password.html')


@login_required
def dashboard_redirect(request):
    """Redirect to the appropriate dashboard based on user role."""
    if request.user.role == UserRole.ADMIN:
        return redirect('admin_dashboard')
    return redirect('employee_dashboard')


@login_required
def profile_view(request):
    """User profile page."""
    employee_profile = None
    try:
        employee_profile = request.user.employee_profile
    except Exception:
        pass

    return render(request, 'profile/profile.html', {
        'employee_profile': employee_profile,
        'page_title': 'My Profile',
    })
