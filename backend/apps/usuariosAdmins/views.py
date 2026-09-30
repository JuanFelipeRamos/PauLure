from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserAdminSerializer

# para obtener el usuario administrador autenticado
class GetCurrentUserAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_admin = UserAdminSerializer(request.user)

        return Response(user_admin.data)

# para obtener todos los usuarios administradores
class GetUsersAdmins(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios_admins = User.objects.all()
        serializer = UserAdminSerializer(usuarios_admins, many=True)
        return Response(serializer.data)
