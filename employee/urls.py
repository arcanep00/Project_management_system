from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('tasks/', views.employee_tasks, name='employee_tasks'),
    path('history/', views.employee_history, name='employee_history'),
]
