from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProfileView

# JWT API endpoints (preserved from Phase 2)
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='api_token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
]
