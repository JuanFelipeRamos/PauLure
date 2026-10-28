#pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProductosSerializers
from .models import Productos

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializers
    permission_classes = [IsAuthenticated]
    filterset_fields = ['categoria']
    search_fields = ['nombre', 'referencia']
    ordering_fields = ['fecha_creacion', 'categoria']

    # para eliminar un producto y mostrar un mensaje de éxito
    def destroy(self, request, *args, **kwargs):
        producto = self.get_object()

        self.perform_destroy(producto)
        return Response({
            "message": "producto eliminado exitosamente"
        })
