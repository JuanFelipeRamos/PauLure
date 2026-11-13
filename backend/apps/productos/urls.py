from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductosViewSet, VarianteProductoViewset

router = DefaultRouter()

router.register(r"variantes", VarianteProductoViewset, basename='variante_producto_views')
router.register(r"", ProductosViewSet, basename='productos_views')

urlpatterns = [
    path('', include(router.urls))
]
