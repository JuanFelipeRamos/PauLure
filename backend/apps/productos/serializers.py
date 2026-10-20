#pylint: disable=no-member
from django.db import transaction
from rest_framework import serializers
from .models import Productos, SecuenciaReferencia, VarianteProducto

class ProductosSerializers(serializers.ModelSerializer):
    variantes_productos = serializers.JSONField(write_only=True)

    class Meta:
        model = Productos
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'referencia',
            'categoria_id',
            'fecha_creacion',
            'variantes_productos'
        ]

        extra_kwargs = {
            'referencia': {'read_only': True},
            'fecha_creacion': {'read_only': True}
        }

    @transaction.atomic
    def create(self, validated_data):
        # crear la referencia única para el producto
        secuencia = (SecuenciaReferencia.objects.select_for_update().first())

        if secuencia is None:
            secuencia = SecuenciaReferencia.objects.create(ultimo_numero=0)

        secuencia.ultimo_numero += 1
        secuencia.save(update_fields=['ultimo_numero'])

        prefijo = validated_data['nombre'].strip()[:3].upper()
        numero_formateado = str(secuencia.ultimo_numero).zfill(3)

        validated_data['referencia'] = f'PAU-{prefijo}-{numero_formateado}'

        # poner la primera letra del nombre y la descripción en mayúscula
        nombre_mayus = validated_data['nombre'].capitalize()
        validated_data['nombre'] = nombre_mayus

        descripcion_mayus = validated_data['descripcion'].capitalize()
        validated_data['descripcion'] = descripcion_mayus

        # crear registros de las variantes de productos (tonos y cantidades)
        variantes = validated_data.pop('variantes_productos')

        instancia_producto = Productos.objects.create(**validated_data)

        for var in variantes:
            VarianteProducto.objects.create(
                producto_id = instancia_producto,
                nombre_tono = var['nombre_tono'].capitalize(),
                color_hex = var['color_hex'],
                cantidad = var['cantidad']
            )

        return instancia_producto
