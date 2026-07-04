from django.contrib import admin
from .models import Arquetipo, Pais, SerFolclorico

@admin.register(Arquetipo)
class ArquetipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion_corta')
    search_fields = ('nombre',)

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_iso', 'continente')
    list_filter = ('continente',)
    search_fields = ('nombre', 'codigo_iso')

@admin.register(SerFolclorico)
class SerFolcloricoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'arquetipo', 'descripcion_breve')
    list_filter = ('arquetipo', 'pais__continente')
    search_fields = ('nombre', 'pais__nombre')
