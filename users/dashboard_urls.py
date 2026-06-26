from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.dashboard_redirect, name='dashboard'),
    path('profile/', web_views.profile_view, name='profile'),
]
