from django.contrib import admin
from .models import Persona

class PersonaAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'apellido', 'email')


admin.site.register(Persona, PersonaAdmin)
