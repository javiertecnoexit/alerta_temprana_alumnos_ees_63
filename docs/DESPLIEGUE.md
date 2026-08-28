# Guía de despliegue — Sistema de Seguimiento Escolar ES63

Esta guía describe cómo desplegar el sistema en un **VPS con EasyPanel en DonWeb**, usando Docker y PostgreSQL.

## Requisitos previos

- Un VPS en DonWeb con **EasyPanel** instalado y accesible.
- Una cuenta en **GitHub** con el repositorio del proyecto subido.
- Un dominio o subdominio (opcional, EasyPanel puede usar la IP del VPS).

## Arquitectura de despliegue

```text
                    Internet
                        │
                        ▼
                Nginx (EasyPanel)  ── TLS/HTTPS
                        │
                        ▼
            Contenedor Docker (Gunicorn + Django)
                        │
                        ▼
              Contenedor PostgreSQL
```

- **Gunicorn** sirve la aplicación Django (2 workers).
- **Whitenoise** sirve los archivos estáticos (CSS/JS) sin servidor aparte.
- **PostgreSQL** como base de datos.
- **EasyPanel** gestiona los contenedores, el proxy inverso (Nginx), los
  certificados SSL y las variables de entorno.

---

## 1. Subir el código a GitHub

Si todavía no lo hiciste:

```bash
# En la carpeta del proyecto (raíz del repo)
git remote add origin https://github.com/TU_USUARIO/alerta_temprana_alumnos_ees_63.git
git branch -M main
git push -u origin main
```

> El repositorio ya incluye el `Dockerfile`, `.dockerignore` y la
> configuración de producción (`config/settings/production.py`).

---

## 2. Crear la base de datos PostgreSQL en EasyPanel

1. En el panel de EasyPanel, ir a **Services**.
2. Crear un nuevo servicio de tipo **PostgreSQL**.
   - Nombre sugerido: `es63-db`
   - Anotar: **usuario**, **contraseña**, **nombre de base de datos** y
     el **host interno** (EasyPanel genera un host interno tipo
     `es63-db` o similar).
3. Esperar a que el servicio esté activo.

---

## 3. Crear la aplicación en EasyPanel

1. Ir a **Projects** → **Create Project**.
2. Elegir tipo **App** (no "Service").
3. Conectar con el repositorio de GitHub (EasyPanel pedirá autorizar el
   acceso a la cuenta).
4. Seleccionar el repositorio y la rama (`main`).
5. En **Build**, elegir **Dockerfile** como método de build (EasyPanel
   detectará el `Dockerfile` automáticamente).
6. Configurar el **puerto** expuesto en `80`.

---

## 4. Configurar variables de entorno

En la configuración de la app, definir las siguientes variables de entorno:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django (generar una larga y aleatoria) | `django-insecure-XXXXX` |
| `DEBUG` | Debe ser `False` en producción | `False` |
| `ALLOWED_HOSTS` | Dominio o IP del sitio, separado por comas | `midominio.com,www.midominio.com` |
| `DB_NAME` | Nombre de la base de datos PostgreSQL | `es63` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `una-contraseña-fuerte` |
| `DB_HOST` | Host interno de PostgreSQL en EasyPanel | `es63-db` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `SECURE_SSL_REDIRECT` | Redirigir HTTP a HTTPS | `True` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes de confianza para CSRF (con protocolo) | `https://midominio.com` |

### Generar una SECRET_KEY segura

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## 5. Vincular la app con la base de datos

1. En EasyPanel, abrir la **app** creada.
2. Ir a la sección **Links / Domains** y conectar el dominio (o usar la
   IP del VPS).
3. Asegurarse de que la app pueda comunicarse con el servicio PostgreSQL:
   - Si EasyPanel lo soporta, vincular los servicios (la app y `es63-db`)
     en la misma red interna.
   - En `DB_HOST` usar el **host interno** del servicio PostgreSQL (no
     `localhost`).

---

## 6. Primer despliegue

1. Hacer clic en **Deploy**.
2. EasyPanel construirá la imagen (instala dependencias, corre
   `collectstatic`) y arrancará Gunicorn.
3. Revisar los **logs** para verificar que no haya errores.

---

## 7. Migraciones y datos iniciales

Las migraciones no se ejecutan automáticamente al construir. Ejecutarlas
una vez desplegado el contenedor. En EasyPanel, usar la consola/terminal
del contenedor de la app:

```bash
# Aplicar migraciones
python manage.py migrate

# Crear el superusuario administrador
python manage.py createsuperuser

# (Opcional) cargar el catálogo de observaciones (27 categorías)
python manage.py loaddata catalogo_observaciones

# (Opcional, solo para prueba) cargar datos de demostración
python manage.py seed_demo
```

> **Importante**: NO usar `seed_demo` en producción real. Es solo para
> pruebas con datos ficticios.

---

## 8. Actualizar el sistema (despliegues posteriores)

1. Hacer push de los cambios a `main`.
2. En EasyPanel, hacer clic en **Deploy** (o habilitar auto-deploy al
   detectar cambios en la rama).
3. Si hay nuevas migraciones, ejecutar:
   ```bash
   python manage.py migrate
   ```

---

## Seguridad y buenas prácticas

- `DEBUG` siempre en `False` en producción.
- `SECRET_KEY` nunca se commitea al repositorio (está en `.env`, que
  está en `.gitignore`; en EasyPanel se define como variable de entorno).
- Usar HTTPS (EasyPanel lo habilita con Let's Encrypt automáticamente).
- Hacer copias de seguridad periódicas del volumen de PostgreSQL.
- El proyecto maneja datos de **menores de edad**. Revisar la normativa
  argentina y de la jurisdicción educativa aplicable antes de cargar
  datos reales.

---

## Estructura de archivos relevante

```text
seguimiento_escolar/
├── Dockerfile                 # Imagen de producción (Gunicorn)
├── .dockerignore              # Archivos excluidos de la imagen
├── requirements.txt           # Django + psycopg2 + gunicorn + whitenoise
├── manage.py
├── config/
│   └── settings/
│       ├── base.py            # Configuración compartida
│       ├── development.py     # Desarrollo local
│       └── production.py      # Producción (seguridad + whitenoise)
└── apps/                      # Aplicaciones del dominio
```
