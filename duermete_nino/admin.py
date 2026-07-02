from django.contrib import admin

from .models import Arquetipo, Pais, SerFolclorico


@admin.register(Arquetipo)
class ArquetipoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_iso", "continente")
    list_filter = ("continente",)


@admin.register(SerFolclorico)
class SerFolcloricoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pais", "arquetipo")
    list_filter = ("pais__continente", "arquetipo")
    search_fields = ("nombre", "descripcion_breve")
