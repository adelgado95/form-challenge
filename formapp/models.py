from django.db import models
import logging

logger = logging.getLogger(__name__)


class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=300)

    def __str__(self):
        return self.nombre + self.apellido



