from django.db import models


class Arquetipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Arquetipo"
        verbose_name_plural = "Arquetipos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Pais(models.Model):
    class Continentes(models.TextChoices):
        EUROPA = "EU", "Europa"
        AMERICA_NORTE = "NA", "Norteamérica"
        AMERICA_LATINA = "LA", "América Latina"
        ASIA = "AS", "Asia"
        AFRICA = "AF", "África"
        OCEANIA = "OC", "Oceanía"

    nombre = models.CharField(max_length=100, db_index=True)
    codigo_iso = models.CharField(
        max_length=3, unique=True, help_text="Código ISO 3166-1 alpha-3"
    )
    continente = models.CharField(max_length=2, choices=Continentes.choices)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iso})"


class SerFolclorico(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion_breve = models.TextField(help_text="Resumen de una línea")
    descripcion_detallada = models.TextField(blank=True)
    pais = models.ForeignKey(
        Pais, on_delete=models.CASCADE, related_name="seres"
    )
    arquetipo = models.ForeignKey(
        Arquetipo, on_delete=models.SET_NULL, null=True, blank=True, related_name="seres"
    )

    class Meta:
        verbose_name = "Ser Folclórico"
        verbose_name_plural = "Seres Folclóricos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
