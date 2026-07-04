# 🗺️ Duérmete Niño

**Cartografía analítica del folclore infantil mundial**

Una plataforma web interactiva que mapea y analiza la mitología y el folclore mundial centrado en la infancia. Descubre más de 100 criaturas, deidades y espíritus que interactúan con los niños, clasificados en 5 arquetipos universales.

![Duérmete Niño](https://img.shields.io/badge/Django-5.x-092E20?logo=django)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-06B6D4?logo=tailwindcss)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ Características

- **🌍 Mapa interactivo** — Explora el folclore infantil por país en un globo terráqueo interactivo
- **👹 100 seres folclóricos** — Base de datos completa con criaturas de los 6 continentes
- **📚 5 arquetipos universales** — Clasificación taxonómica: Devoradora, Secuestrador, Espíritu Acuático, Niño Fantasma, Protector
- **🌙 Dark mode inmersivo** — Interfaz oscura tipo "fantasía" con Tailwind CSS v4
- **🔌 API REST** — Endpoints JSON para consumir los datos desde cualquier frontend
- **🚀 Despliegue en Render** — Configurado para deploy continuo

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Django 5 (Python) |
| Frontend | Tailwind CSS v4 (CDN), Vanilla JavaScript |
| Base de Datos | SQLite (desarrollo) / PostgreSQL (producción) |
| Servidor | Gunicorn + Whitenoise |
| Despliegue | Render |

---

## 🚀 Inicio Rápido

### Requisitos

- Python 3.11+
- pip

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/duermete-nino.git
cd duermete-nino

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Cargar datos iniciales (100 seres folclóricos)
python manage.py loaddata folclore_inicial.json

# Iniciar servidor de desarrollo
python manage.py runserver
```

Visita [http://localhost:8000](http://localhost:8000) 🎉

---

## 📁 Estructura del Proyecto

```
duermete-nino/
├── config/                  # Configuración de Django
│   ├── settings.py          # Settings principales
│   ├── urls.py              # URL routing raíz
│   └── wsgi.py              # WSGI para producción
├── duermete_nino/           # Aplicación principal
│   ├── models.py            # Modelos: Arquetipo, Pais, SerFolclorico
│   ├── views.py             # Vistas basadas en funciones + API
│   ├── urls.py              # URLs de la aplicación
│   ├── admin.py             # Configuración del admin
│   ├── templates/           # Templates HTML
│   │   └── duermete_nino/
│   │       ├── home.html        # Página principal (mapa)
│   │       ├── arquetipos.html  # Los 5 arquetipos
│   │       └── acerca_de.html   # Información del proyecto
│   └── fixtures/            # Datos precargados
│       └── folclore_inicial.json  # 100 seres de 47 países
├── static/                  # Archivos estáticos
│   ├── css/
│   └── js/
│       └── mapa.js          # Lógica del mapa interactivo
├── manage.py
├── requirements.txt
├── render.yaml              # Configuración de despliegue
└── build.sh                 # Script de construcción
```

---

## 🔌 API REST

| Endpoint | Descripción |
|----------|------------|
| `GET /api/seres/` | Lista completa de todos los seres folclóricos |
| `GET /api/pais/{codigo_iso}/seres/` | Seres de un país específico (ej: `/api/pais/ES/seres/`) |
| `GET /api/ser/{id}/` | Detalle completo de un ser por ID |

### Ejemplo de respuesta

```json
GET /api/pais/IS/seres/

{
  "pais": "Islandia",
  "continente": "Europa",
  "seres": [
    {
      "id": 1,
      "nombre": "Grýla",
      "arquetipo": "La devoradora de niños",
      "descripcion_breve": "Devora niños desobedientes en Navidad.",
      "descripcion_detallada": "Grýla es una gigantesca criatura..."
    }
  ]
}
```

---

## 📊 Datos

- **5 Arquetipos**: Devoradora de niños, Secuestrador/Castigador, Espíritu acuático, Niño fantasma, Protector del hogar
- **47 Países** en los 6 continentes
- **100 Seres folclóricos** documentados con descripciones detalladas

---

## 🚀 Despliegue en Render

El proyecto incluye configuración lista para Render:

```yaml
# render.yaml
services:
  - type: web
    name: duermete-nino-app
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"
```

Variables de entorno necesarias:
- `DJANGO_SECRET_KEY`: Clave secreta de Django
- `DJANGO_DEBUG`: `False` en producción
- `DJANGO_ALLOWED_HOSTS`: Hosts permitidos (`.onrender.com`)

---

## 📝 Licencia

MIT © 2026
