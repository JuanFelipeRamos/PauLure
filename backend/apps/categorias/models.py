from django.db import models

class Categorias(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
