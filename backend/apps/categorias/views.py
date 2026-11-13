#pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from .serializers import CategoriasSerializers
from .models import Categorias

class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializers
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)

            return Response({
                "message": "categoría eliminada exitosamente"
            })
        except ProtectedError:
            return Response(
                {'detail': 'no se puede eliminar la categoría porque tiene productos asociados.'},
                status=status.HTTP_409_CONFLICT,
            )
