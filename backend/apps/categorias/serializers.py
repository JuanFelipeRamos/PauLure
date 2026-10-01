from rest_framework import serializers
from .models import Categorias

class CategoriasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = ['id', 'nombre']
