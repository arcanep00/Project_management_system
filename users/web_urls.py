from django.urls import path
from . import web_views

urlpatterns = [
    path('login/', web_views.login_view, name='login'),
    path('logout/', web_views.logout_view, name='logout'),
    path('forgot-password/', web_views.forgot_password_view, name='forgot_password'),
]
