#pylint: disable=no-member
import logging
from io import BytesIO
from PIL import Image  # pylint: disable=import-error
from django.core.files.uploadedfile import InMemoryUploadedFile
import cloudinary.uploader
from .models import ImagenProducto, VarianteProducto

logger = logging.getLogger(__name__)


def comprimir_imagen(image_file, max_size_kb=2000):
    img = Image.open(image_file)
    original_name = getattr(image_file, 'name', 'imagen.jpg') or 'imagen.jpg'
    base_name = original_name.rsplit('.', 1)[0]

    # si ya cumple tamaño, devolver tal cual
    if image_file.size <= max_size_kb * 1024:
        return image_file

    # convertir a RGB si tiene transparencia o paleta
    if img.mode in ('RGBA', 'P', 'LA'):
        img = img.convert('RGB')

    buffer = BytesIO()
    quality = 95
    while quality > 10:
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        if buffer.tell() <= max_size_kb * 1024:
            break
        quality -= 5

    buffer.seek(0)

    # envolver como InMemoryUploadedFile con nombre .jpg
    nuevo_nombre = f'{base_name}.jpg'
    return InMemoryUploadedFile(
        file=buffer,
        field_name=None,
        name=nuevo_nombre,
        content_type='image/jpeg',
        size=buffer.getbuffer().nbytes,
        charset=None
    )


def primera_mayuscula(texto):
    return texto[:1].upper() + texto[1:]


def borrar_imagen_cloudinary(public_id):
    try:
        cloudinary.uploader.destroy(public_id, invalidate=True)
    except Exception:
        logger.exception('No se pudo borrar la imagen %s de Cloudinary', public_id)


def crear_imagenes(producto, imagenes):
    if not imagenes:
        return

    for i, archivo in enumerate(imagenes):
        try:
            archivo_comprimido = comprimir_imagen(archivo, max_size_kb=2000)
            ImagenProducto.objects.create(
                producto=producto,
                imagen=archivo_comprimido,
                orden=i
            )
        except Exception:
            logger.exception('Error al procesar imagen %s', archivo.name)
            raise


def crear_variantes(producto, variantes):
    for var in variantes:
        nombre_tono = var.get('nombre_tono')
        VarianteProducto.objects.create(
            producto=producto,
            nombre_tono=primera_mayuscula(nombre_tono) if nombre_tono else None,
            color_hex=var.get('color_hex'),
            cantidad=var['cantidad'],
        )
