from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import UserRole
from .models import Employee


@login_required
def employee_dashboard(request):
    """Employee-facing dashboard."""
    employee_profile = getattr(request.user, 'employee_profile', None)

    context = {
        'page_title': 'My Dashboard',
        'employee_profile': employee_profile,
        # Placeholder statistics
        'tasks_pending': 5,
        'tasks_completed': 12,
        'audio_uploads': 3,
        'announcements': [
            {'title': 'Team Meeting', 'body': 'Scheduled for Friday 3 PM.', 'date': 'Today'},
            {'title': 'New Policy Update', 'body': 'Please review the updated HR policy.', 'date': 'Yesterday'},
        ],
    }
    return render(request, 'dashboard/employee_dashboard.html', context)


@login_required
def upload_audio(request):
    """Audio upload UI — placeholder."""
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        if audio_file:
            messages.success(
                request,
                f'File "{audio_file.name}" uploaded successfully. Processing will begin shortly.'
            )
        else:
            messages.error(request, 'Please select an audio file to upload.')
        return redirect('upload_audio')

    return render(request, 'employee/upload_audio.html', {
        'page_title': 'Upload Audio',
    })


@login_required
def employee_tasks(request):
    """Employee tasks view — placeholder."""
    # Placeholder task data
    tasks = [
        {'id': 1, 'title': 'Complete project report', 'due': '2026-06-30', 'status': 'Pending', 'priority': 'High'},
        {'id': 2, 'title': 'Attend team training', 'due': '2026-06-28', 'status': 'In Progress', 'priority': 'Medium'},
        {'id': 3, 'title': 'Submit timesheet', 'due': '2026-06-27', 'status': 'Completed', 'priority': 'Low'},
        {'id': 4, 'title': 'Review code changes', 'due': '2026-07-02', 'status': 'Pending', 'priority': 'High'},
    ]
    return render(request, 'employee/tasks.html', {
        'page_title': 'My Tasks',
        'tasks': tasks,
    })


@login_required
def employee_history(request):
    """Employee activity history — placeholder."""
    history = [
        {'date': '2026-06-25', 'action': 'Audio Upload', 'description': 'Uploaded meeting_notes.mp3'},
        {'date': '2026-06-24', 'action': 'Task Completed', 'description': 'Completed Q2 Report'},
        {'date': '2026-06-23', 'action': 'Profile Updated', 'description': 'Updated phone number'},
        {'date': '2026-06-22', 'action': 'Login', 'description': 'Logged in from Chrome/Windows'},
    ]
    return render(request, 'employee/history.html', {
        'page_title': 'My History',
        'history': history,
    })
