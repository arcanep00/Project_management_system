from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from users.models import User, UserRole
from employee.models import Employee
from .forms import EmployeeCreateForm, EmployeeEditForm, EmployeeProfileForm


def admin_required(view_func):
    """Decorator: requires authenticated user with ADMIN role."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != UserRole.ADMIN:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('employee_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    """Admin dashboard with summary statistics."""
    total_employees = User.objects.filter(role=UserRole.EMPLOYEE).count()
    active_employees = Employee.objects.filter(status='ACTIVE').count()
    on_leave = Employee.objects.filter(status='ON_LEAVE').count()
    total_departments = (
        User.objects.exclude(department='')
        .values('department').distinct().count()
    )
    recent_employees = (
        User.objects.filter(role=UserRole.EMPLOYEE)
        .order_by('-date_joined')[:5]
    )

    context = {
        'page_title': 'Admin Dashboard',
        'total_employees': total_employees,
        'active_employees': active_employees,
        'on_leave': on_leave,
        'total_departments': total_departments,
        'recent_employees': recent_employees,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@admin_required
def employee_list(request):
    """List all employees with search and department filter."""
    query = request.GET.get('q', '')
    dept_filter = request.GET.get('department', '')

    employees = User.objects.filter(role=UserRole.EMPLOYEE).order_by('-date_joined')

    if query:
        from django.db.models import Q
        employees = employees.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    if dept_filter:
        employees = employees.filter(department__icontains=dept_filter)

    departments = (
        User.objects.exclude(department='')
        .values_list('department', flat=True).distinct()
    )

    context = {
        'page_title': 'Employee Management',
        'employees': employees,
        'query': query,
        'dept_filter': dept_filter,
        'departments': departments,
        'total_count': employees.count(),
    }
    return render(request, 'employee/list.html', context)


@admin_required
def employee_add(request):
    """Create a new User account and Employee profile."""
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        department=form.cleaned_data.get('department', ''),
                        role=form.cleaned_data['role'],
                    )
                    Employee.objects.create(
                        user=user,
                        phone=form.cleaned_data.get('phone', ''),
                        position=form.cleaned_data.get('position', ''),
                        employment_type=form.cleaned_data.get('employment_type', 'FULL_TIME'),
                        joining_date=form.cleaned_data.get('joining_date'),
                    )
                messages.success(
                    request,
                    f'Employee {user.get_full_name() or user.username} created successfully.'
                )
                return redirect('employee_list')
            except Exception as e:
                messages.error(request, f'Error creating employee: {str(e)}')
    else:
        form = EmployeeCreateForm()

    return render(request, 'employee/add.html', {
        'form': form,
        'page_title': 'Add Employee',
    })


@admin_required
def employee_detail(request, pk):
    """View full details of an employee."""
    employee_user = get_object_or_404(User, pk=pk)
    employee_profile = getattr(employee_user, 'employee_profile', None)

    return render(request, 'employee/detail.html', {
        'employee_user': employee_user,
        'employee_profile': employee_profile,
        'page_title': f'{employee_user.get_full_name() or employee_user.username}',
    })


@admin_required
def employee_edit(request, pk):
    """Edit an employee's User and profile data."""
    employee_user = get_object_or_404(User, pk=pk)
    employee_profile, _ = Employee.objects.get_or_create(user=employee_user)

    if request.method == 'POST':
        user_form = EmployeeEditForm(request.POST, instance=employee_user)
        profile_form = EmployeeProfileForm(request.POST, instance=employee_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_detail', pk=pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        user_form = EmployeeEditForm(instance=employee_user)
        profile_form = EmployeeProfileForm(instance=employee_profile)

    return render(request, 'employee/edit.html', {
        'employee_user': employee_user,
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': f'Edit — {employee_user.get_full_name() or employee_user.username}',
    })


@admin_required
def employee_delete(request, pk):
    """Confirm and delete an employee."""
    employee_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        name = employee_user.get_full_name() or employee_user.username
        employee_user.delete()
        messages.success(request, f'Employee {name} has been deleted.')
        return redirect('employee_list')

    return render(request, 'employee/delete_confirm.html', {
        'employee_user': employee_user,
        'page_title': 'Delete Employee',
    })


@admin_required
def reports_view(request):
    """Reports dashboard — summary data."""
    dept_breakdown = (
        User.objects.filter(role=UserRole.EMPLOYEE)
        .exclude(department='')
        .values('department')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    employment_breakdown = (
        Employee.objects.values('employment_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    status_breakdown = (
        Employee.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'page_title': 'Reports',
        'dept_breakdown': dept_breakdown,
        'employment_breakdown': employment_breakdown,
        'status_breakdown': status_breakdown,
        'total_users': User.objects.count(),
        'total_admins': User.objects.filter(role=UserRole.ADMIN).count(),
        'total_employees': User.objects.filter(role=UserRole.EMPLOYEE).count(),
    }
    return render(request, 'reports/reports.html', context)


@admin_required
def settings_view(request):
    """Settings page — placeholder UI."""
    if request.method == 'POST':
        messages.success(request, 'Settings saved successfully.')
        return redirect('settings')
    return render(request, 'settings/settings.html', {'page_title': 'Settings'})
