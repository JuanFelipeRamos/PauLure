#pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CategoriasSerializers
from .models import Categorias
from apps.productos.models import Productos

class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializers
    permission_classes = [IsAuthenticated]

    # para eliminar una categoría y mostrar un mensaje de éxito
    def destroy(self, request, *args, **kwargs):
        categoria = self.get_object()

        # no permitir eliminar si hay productos asociados
        productos_asociados = Productos.objects.filter(categoria_id=categoria.id)

        if productos_asociados.exists():
            return Response({
                "error": "no se puede eliminar la categoría si hay productos asociados"
            }, status=409)

        self.perform_destroy(categoria)
        return Response({
            "message": "categoria eliminada exitosamente"
        })
