from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web authentication (session-based)
    path('auth/', include('users.web_urls')),

    # Role-based dashboard redirect
    path('dashboard/', include('users.dashboard_urls')),

    # Admin panel (employee management, reports, settings)
    path('admin-panel/', include('admin_panel.urls')),

    # Employee-facing pages
    path('employee/', include('employee.urls')),

    # REST API (JWT-based — preserved from Phase 2)
    path('api/auth/', include('users.urls')),

    # Root redirect
    path('', lambda req: redirect('login'), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'users.views.custom_404'
