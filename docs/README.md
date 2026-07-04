# Documentación - Duérmete Niño

## Estructura del Proyecto

- `config/` - Configuración del proyecto Django
- `duermete_nino/` - Aplicación principal con modelos, vistas, templates y fixtures
- `static/` - Archivos estáticos (JS, CSS)

## Próximas Implementaciones

Ver [progreso_y_futuro.md](progreso_y_futuro.md) para la hoja de ruta del proyecto.

## API Reference

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Página principal con el mapa interactivo |
| `/arquetipos/` | GET | Los 5 arquetipos universales |
| `/acerca-de/` | GET | Información del proyecto |
| `/api/seres/` | GET | JSON con todos los seres |
| `/api/pais/{codigo}/seres/` | GET | JSON con seres de un país |
| `/api/ser/{id}/` | GET | JSON con detalle de un ser |
