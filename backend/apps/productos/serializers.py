#pylint: disable=no-member
import json
from django.db import transaction
from rest_framework import serializers
from .models import Productos, SecuenciaReferencia, VarianteProducto

class VarianteInputSerializer(serializers.Serializer):
    nombre_tono = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    color_hex = serializers.CharField(
        max_length=12,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    cantidad = serializers.IntegerField(min_value=0)


class VariantesJSONField(serializers.Field):
    """acepta el arreglo como string JSON (form-data) o como lista real (JSON)."""

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except ValueError as exc:
                raise serializers.ValidationError('debe ser un JSON válido.') from exc

        serializer = VarianteInputSerializer(data=data, many=True, allow_empty=False)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def to_representation(self, value):
        return value


class ProductosSerializers(serializers.ModelSerializer):
    imgs = serializers.ImageField(required=False, allow_null=True)
    variantes_productos = VariantesJSONField(write_only=True)

    class Meta:
        model = Productos
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'imgs',
            'referencia',
            'categoria',
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
            nombre_tono = var.get('nombre_tono')

            VarianteProducto.objects.create(
                producto = instancia_producto,
                nombre_tono = nombre_tono.capitalize() if nombre_tono else None,
                color_hex=var.get('color_hex'),
                cantidad = var['cantidad']
            )

        return instancia_producto
