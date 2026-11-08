#pylint: disable=no-member
import logging
import cloudinary.uploader
from .models import ImagenProducto, VarianteProducto

logger = logging.getLogger(__name__)


def primera_mayuscula(texto):
    return texto[:1].upper() + texto[1:]


def borrar_imagen_cloudinary(public_id):
    try:
        cloudinary.uploader.destroy(public_id, invalidate=True)
    except Exception:
        logger.exception('No se pudo borrar la imagen %s de Cloudinary', public_id)


def crear_imagenes(producto, archivos):
    for orden, archivo in enumerate(archivos):
        ImagenProducto.objects.create(producto=producto, imagen=archivo, orden=orden)


def crear_variantes(producto, variantes):
    for var in variantes:
        nombre_tono = var.get('nombre_tono')
        VarianteProducto.objects.create(
            producto=producto,
            nombre_tono=primera_mayuscula(nombre_tono) if nombre_tono else None,
            color_hex=var.get('color_hex'),
            cantidad=var['cantidad'],
        )
