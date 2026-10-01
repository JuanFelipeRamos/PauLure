#pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CategoriasSerializers
from .models import Categorias

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializers
    permission_classes = [IsAuthenticated]

    # para eliminar una categoría y mostrar un mensaje de éxito
    def destroy(self, request, *args, **kwargs):
        categoria = self.get_object()
        self.perform_destroy(categoria)
        return Response({
            "message": "categoria eliminada exitosamente"
        })
