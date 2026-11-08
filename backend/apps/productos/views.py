#pylint: disable=no-member
from rest_framework import viewsets
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import ProductosSerializers, VarianteProductoSerializer
from .models import Productos, VarianteProducto
from .utils import borrar_imagen_cloudinary

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializers
    permission_classes = [IsAuthenticated]
    filterset_fields = ['categoria']
    search_fields = ['nombre', 'referencia']
    ordering_fields = ['fecha_creacion', 'categoria']

    # para eliminar las imágenes de cloudinary al borrar un producto
    @transaction.atomic
    def perform_destroy(self, instance):
        public_ids = [img.imagen.public_id for img in instance.imagenes.all()]
        instance.delete()

        for pid in public_ids:
            transaction.on_commit(lambda pid=pid: borrar_imagen_cloudinary(pid))

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
