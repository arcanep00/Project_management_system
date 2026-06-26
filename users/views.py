from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import UserSerializer
from .models import User


# ------------------------------------------------------------------
# REST API View (Phase 2 — preserved)
# ------------------------------------------------------------------

class ProfileView(APIView):
    """JWT-authenticated profile endpoint."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ------------------------------------------------------------------
# Custom error handlers
# ------------------------------------------------------------------

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)
