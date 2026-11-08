#pylint: disable=no-member
from rest_framework import serializers
from .models import Categorias

class CategoriasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = ['id', 'nombre']

    def create(self, validate_data):
        validate_data['nombre'] = validate_data['nombre'].capitalize()

        return Categorias.objects.create(**validate_data)
