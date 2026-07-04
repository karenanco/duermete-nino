from django.db import models


class Arquetipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del arquetipo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Arquetipo"
        verbose_name_plural = "Arquetipos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def descripcion_corta(self):
        return self.descripcion[:80] + '...' if len(self.descripcion) > 80 else self.descripcion
    descripcion_corta.short_description = "Descripción"


class Pais(models.Model):
    class Continentes(models.TextChoices):
        AFRICA = 'AF', 'África'
        ASIA = 'AS', 'Asia'
        EUROPA = 'EU', 'Europa'
        NORTEAMERICA = 'NA', 'Norteamérica'
        OCEANIA = 'OC', 'Oceanía'
        SURAMERICA = 'SA', 'Sudamérica'

    nombre = models.CharField(max_length=100, verbose_name="Nombre del país")
    codigo_iso = models.CharField(max_length=3, unique=True, verbose_name="Código ISO")
    continente = models.CharField(max_length=2, choices=Continentes.choices, verbose_name="Continente")

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iso})"


class SerFolclorico(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del ser")
    descripcion_breve = models.TextField(max_length=300, verbose_name="Descripción breve")
    descripcion_detallada = models.TextField(blank=True, verbose_name="Descripción detallada")
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='seres', verbose_name="País de origen")
    arquetipo = models.ForeignKey(Arquetipo, on_delete=models.SET_NULL, null=True, blank=True, related_name='seres', verbose_name="Arquetipo")

    class Meta:
        verbose_name = "Ser Folclórico"
        verbose_name_plural = "Seres Folclóricos"
        ordering = ['pais__nombre', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"
