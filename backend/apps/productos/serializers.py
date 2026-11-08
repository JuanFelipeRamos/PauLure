#pylint: disable=no-member
import json
from django.db import transaction
from rest_framework import serializers
from .models import Productos, SecuenciaReferencia, VarianteProducto, ImagenProducto
from .utils import (primera_mayuscula, borrar_imagen_cloudinary, crear_imagenes, crear_variantes)

MIN_IMAGENES = 2
MAX_IMAGENES = 3

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


# para peticiones GET, PATCH Y DELETE
class VarianteProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarianteProducto
        fields = ['id', 'nombre_tono', 'color_hex', 'cantidad']


# para mostrar las imágenes
class ImagenProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(read_only=True)

    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'orden']


class ProductosSerializers(serializers.ModelSerializer):
    variantes = VarianteProductoSerializer(many=True, read_only=True)

    imgs = serializers.ListField(
        child=serializers.ImageField(),
        max_length=MAX_IMAGENES,
        write_only=True,
    )
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    orden_imagenes = serializers.JSONField(required=False, write_only=True)
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
            'orden_imagenes',
            'referencia',
            'categoria',
            'fecha_creacion',
            'variantes_productos',
            'variantes'
        ]

        extra_kwargs = {
            'referencia': {'read_only': True},
            'fecha_creacion': {'read_only': True}
        }

    def validate_nombre(self, value):
        return primera_mayuscula(value.strip())

    def validate_descripcion(self, value):
        return primera_mayuscula(value.strip())

    def validate_imgs(self, value):
        if self.instance is None and len(value) < MIN_IMAGENES:
            raise serializers.ValidationError(
                f'Debes enviar al menos {MIN_IMAGENES} imágenes.'
            )
        return value

    def validate_orden_imagenes(self, value):
        es_valido = isinstance(value, list) and all(
            x == 'nueva' or (isinstance(x, int) and not isinstance(x, bool))
            for x in value
        )
        if not es_valido:
            raise serializers.ValidationError('Debe ser una lista de ids enteros y/o "nueva".')
        return value

    def validate(self, attrs):
        if self.instance is None:
            return attrs

        archivos = attrs.get('imgs', None)
        orden = attrs.get('orden_imagenes')

        if orden is None:
            if archivos:
                raise serializers.ValidationError(
                    {'orden_imagenes': 'Es obligatorio cuando se envían imágenes.'}
                )
            return attrs

        conservar = [x for x in orden if x != 'nueva']
        actuales = set(self.instance.imagenes.values_list('id', flat=True))
        nuevas_count = orden.count('nueva')

        if not MIN_IMAGENES <= len(orden) <= MAX_IMAGENES:
            msg = f'El producto debe quedar con entre {MIN_IMAGENES} y {MAX_IMAGENES} imágenes.'
        elif len(conservar) != len(set(conservar)):
            msg = 'Hay ids repetidos.'
        elif not set(conservar) <= actuales:
            msg = 'Hay ids que no pertenecen a este producto.'
        elif nuevas_count > 0 and (archivos is None or len(archivos) != nuevas_count):
            msg = f'Se esperan {nuevas_count} archivos nuevos en "imgs", pero se recibieron {len(archivos) if archivos else 0}.'
        else:
            return attrs
        raise serializers.ValidationError({'orden_imagenes': msg})

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

        # crear registros de las variantes de productos (tonos y cantidades)
        variantes = validated_data.pop('variantes_productos')
        validated_data.pop('orden_imagenes', None)
        imagenes = validated_data.pop('imgs', None)

        instancia_producto = Productos.objects.create(**validated_data)

        crear_variantes(instancia_producto, variantes)

        crear_imagenes(instancia_producto, imagenes)

        return instancia_producto

    @transaction.atomic
    def update(self, instance, validated_data):
        archivos = validated_data.pop('imgs', None)
        orden = validated_data.pop('orden_imagenes', None)
        variantes = validated_data.pop('variantes_productos', None)

        instance = super().update(instance, validated_data)

        if variantes is not None:
            crear_variantes(instance, variantes)

        if orden is not None:
            actuales = {img.id: img for img in instance.imagenes.all()}

            # las que no aparecen en la lista se eliminan
            a_borrar = [img for img_id, img in actuales.items() if img_id not in orden]
            public_ids = [img.imagen.public_id for img in a_borrar]
            for img in a_borrar:
                img.delete()

            if 'nueva' in orden:
                if archivos is None:
                    raise serializers.ValidationError(
                        {'imgs': 'Se requieren archivos cuando se usa "nueva" en el orden.'}
                    )
                nuevos = iter(archivos)
            else:
                nuevos = None  # no hay imágenes nuevas

            conservadas = []

            for posicion, item in enumerate(orden):
                if item == 'nueva':
                    ImagenProducto.objects.create(
                        producto=instance, imagen=next(nuevos), orden=posicion
                    )
                else:
                    actuales[item].orden = posicion
                    conservadas.append(actuales[item])

            ImagenProducto.objects.bulk_update(conservadas, ['orden'])

            # Cloudinary se borra solo si MySQL confirmó todo
            for pid in public_ids:
                transaction.on_commit(lambda pid=pid: borrar_imagen_cloudinary(pid))

        return instance
