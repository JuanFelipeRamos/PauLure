#pylint: disable=no-member
import logging
import cloudinary.uploader
from .models import ImagenProducto

logger = logging.getLogger(__name__)


def borrar_imagen_cloudinary(public_id):
    try:
        cloudinary.uploader.destroy(public_id, invalidate=True)
    except Exception:
        logger.exception('No se pudo borrar la imagen %s de Cloudinary', public_id)


def crear_imagenes(producto, archivos):
    for orden, archivo in enumerate(archivos):
        ImagenProducto.objects.create(producto=producto, imagen=archivo, orden=orden)
