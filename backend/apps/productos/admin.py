from django.contrib import admin
from .models import Productos, SecuenciaReferencia, VarianteProducto

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'referencia', 'categoria_id', 'fecha_creacion']

@admin.register(SecuenciaReferencia)
class SecuenciaReferenciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'ultimo_numero']

@admin.register(VarianteProducto)
class VarianteProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto_id', 'nombre_tono', 'color_hex', 'cantidad']
