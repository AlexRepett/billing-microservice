# Microservicio de Facturación

> Sistema de facturación independiente desarrollado con Django, diseñado para integrarse con múltiples plataformas mediante API REST.

**Estado:** 🚧 Fase 1 - Setup Inicial (Completada)

---

## 📋 Stack Tecnológico

- **Backend:** Django 4.2.x + Django REST Framework
- **Base de Datos:** PostgreSQL 
- **Lenguaje:** Python 3.x
- **IDE:** Visual Studio Code
- **Contenedores:** Docker (Fase 3 - Pendiente)

---

## ✨ Características Actuales

- ✅ Proyecto Django configurado
- ✅ App `billing` creada
- ✅ Conexión a PostgreSQL establecida
- ✅ Panel de administración Django funcional
- ✅ CORS configurado para desarrollo
- ✅ Variables de entorno con python-decouple

---

## 🔧 Requisitos Previos

Antes de clonar/ejecutar el proyecto, necesitas tener instalado:

- Python 3.10 o superior
- PostgreSQL 12 o superior
- Git

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio (cuando aplique)
```bash
git clone (https://github.com/AlexRepett/billing-microservice.git)
cd billing-microservice
```

### 2. Crear y activar entorno virtual
```bash
# Windows PowerShell
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r src/requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con:
```env
# Database
DB_NAME=billing_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
```

### 5. Crear la base de datos

Desde pgAdmin o psql, crea la base de datos:
```sql
CREATE DATABASE billing_db;
```

### 6. Ejecutar migraciones
```bash
python src/manage.py migrate
```

### 7. Crear superusuario
```bash
python src/manage.py createsuperuser
```

### 8. Iniciar servidor de desarrollo
```bash
python src/manage.py runserver
```

Accede a:
- **Aplicación:** http://localhost:8000
- **Panel Admin:** http://localhost:8000/admin

---

## 📁 Estructura del Proyecto
```
billing-microservice/
├── .env                    # Variables de entorno (no versionado)
├── .gitignore              # Archivos ignorados por Git
├── README.md               # Este archivo
├── venv/                   # Entorno virtual Python
├── src/
│   ├── manage.py           # Script de gestión Django
│   ├── requirements.txt    # Dependencias de desarrollo
│   ├── requirements-production.txt  # Dependencias de producción
│   ├── config/             # Configuración del proyecto Django
│   │   ├── settings.py     # Configuración principal
│   │   ├── urls.py         # URLs principales
│   │   ├── wsgi.py         # Entry point WSGI
│   │   └── asgi.py         # Entry point ASGI
│   └── billing/            # App de facturación
│       ├── models.py       # Modelos de datos (próximo)
│       ├── views.py        # Vistas y API endpoints (próximo)
│       ├── serializers.py  # Serializadores DRF (próximo)
│       └── admin.py        # Configuración del admin
├── docker/                 # Configuración Docker (Fase 3)
├── docs/                   # Documentación adicional
└── scripts/                # Scripts de automatización
```

---

## 🎯 Roadmap

### ✅ Fase 1 - Setup Inicial (COMPLETADA)
- Configuración de entorno virtual
- Instalación de Django y dependencias
- Conexión con PostgreSQL
- Estructura base del proyecto

### 🔜 Fase 2 - Desarrollo del Microservicio (PRÓXIMO)
- Diseño de modelos (Factura, Cliente, Producto)
- Implementación de API REST con DRF
- Creación de vistas web para gestión
- Templates y archivos estáticos
- Generación de PDFs

### 📦 Fase 3 - Contenedorización y Deployment
- Dockerfile
- Docker Compose
- Configuración para producción
- Integración con Vortx CRM

---

## 🔐 Seguridad

- ⚠️ **NUNCA** subas el archivo `.env` a Git
- ⚠️ Cambia `SECRET_KEY` antes de ir a producción
- ⚠️ Configura `CORS_ALLOWED_ORIGINS` con dominios específicos en producción

---

## 👩‍💻 Desarrollo

**Creado por:** Veronica Alexis Repetto Tinoco
**Fecha de inicio:** Febrero 2026  
**Objetivo:** Microservicio de facturación para integración con Vortx CRM

---

## 📝 Notas

- El proyecto usa `python-decouple` para gestión de variables de entorno
- CORS está configurado en modo "allow all" solo para desarrollo
- Para producción, revisar configuraciones comentadas en `settings.py`
