#pylint: disable=no-member
import json
from django.db import transaction
from rest_framework import serializers
from .models import Productos, SecuenciaReferencia, VarianteProducto, ImagenProducto
from .utils import borrar_imagen_cloudinary, crear_imagenes

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


# para mostrar las imágenes
class ImagenProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(read_only=True)

    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'orden']


class ProductosSerializers(serializers.ModelSerializer):
    imgs = serializers.ListField(
        child=serializers.ImageField(),
        min_length=2,
        max_length=3,
        write_only=True,
    )
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    id_img = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    variantes_productos = VariantesJSONField(write_only=True)

    class Meta:
        model = Productos
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'imgs',
            'imagenes',
            'id_img',
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
        imagenes = validated_data.pop('imgs', [])

        instancia_producto = Productos.objects.create(**validated_data)

        for var in variantes:
            nombre_tono = var.get('nombre_tono')

            VarianteProducto.objects.create(
                producto = instancia_producto,
                nombre_tono = nombre_tono.capitalize() if nombre_tono else None,
                color_hex=var.get('color_hex'),
                cantidad = var['cantidad']
            )

        crear_imagenes(instancia_producto, imagenes)

        return instancia_producto

    @transaction.atomic
    def update(self, instance, validated_data):
        imagenes = validated_data.pop('imgs', None)
        ids = validated_data.pop('id_img', None)

        # para editar imágenes (TODAS, HAY QUE HACER PARA PODER EDITAR UNA SOLA) de un producto
        if imagenes is not None:
            # obtiene el public_id de cada imagen actual del producto
            anteriores = [img.imagen.public_id for img in instance.imagenes.all()]

            # borra de MySQL las imágenes viejas
            instance.imagenes.all().delete()

            crear_imagenes(instance, imagenes)

            for public_id in anteriores:
                transaction.on_commit(lambda pid=public_id: borrar_imagen_cloudinary(pid))

        # para editar el orden de las imágenes de un producto
        if ids is not None:
            actuales = {img.id: img for img in instance.imagenes.all()}

            if len(ids) != len(set(ids)) or set(ids) != set(actuales):
                raise serializers.ValidationError({
                    'id_img': 'Debe incluir exactamente las imágenes actuales, sin repetir.'
                })

            for orden, id_img in enumerate(ids):
                actuales[id_img].orden = orden
            ImagenProducto.objects.bulk_update(actuales.values(), ['orden'])

        return instance
