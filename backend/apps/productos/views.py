#pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import ProductosSerializers, VarianteProductoSerializer
from .models import Productos, VarianteProducto

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

class VarianteProductoViewset(viewsets.ModelViewSet):
    queryset = VarianteProducto.objects.all()
    serializer_class = VarianteProductoSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # verifica si es la última variante del producto
        if VarianteProducto.objects.filter(producto=instance.producto).count() <= 1:
            raise ValidationError(
                "no se puede eliminar la última variante del producto."
            )
        instance.delete()
