from django.db import models
from cloudinary.models import CloudinaryField
from apps.categorias.models import Categorias

class Productos(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imgs = CloudinaryField('image', blank=True, null=True)
    referencia = models.CharField(max_length=15, blank=True, null=True, unique=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

# tabla para llevar el control de la secuencia de las referencias de los productos
class SecuenciaReferencia(models.Model):
    ultimo_numero = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Secuencia de referencia'
        verbose_name_plural = 'Secuencias de referencias'

# tabla para administrar tonos y cantidades de productos
class VarianteProducto(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, blank=True, null=True)
    nombre_tono = models.CharField(max_length=20, blank=True, null=True)
    color_hex = models.CharField(max_length=12, blank=True, null=True)
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Variante de producto'
        verbose_name_plural = 'Variantes de productos'
