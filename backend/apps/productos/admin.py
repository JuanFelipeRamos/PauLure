from django.contrib import admin
from .models import Productos, SecuenciaReferencia, VarianteProducto

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'referencia', 'categoria', 'fecha_creacion']

@admin.register(SecuenciaReferencia)
class SecuenciaReferenciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'ultimo_numero']

@admin.register(VarianteProducto)
class VarianteProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'nombre_tono', 'color_hex', 'cantidad']
