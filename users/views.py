from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ProfileView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )
