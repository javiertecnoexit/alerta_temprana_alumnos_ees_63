# Sistema de Seguimiento Escolar — Escuela Secundaria N.º 63

Sistema de alerta temprana para alumnos de la Escuela Secundaria N.º 63.
Permite a los docentes registrar observaciones breves y estructuradas
sobre la trayectoria de los alumnos, y al equipo directivo analizarlas
transversalmente para detectar tempranamente necesidades de acompañamiento
y oportunidades de desarrollo.

## Institución

- Escuela Secundaria N.º 63
- Turnos: mañana y tarde

## Stack Tecnológico

- **Backend:** Python + Django 4.2
- **Base de datos:** PostgreSQL
- **Servidor WSGI:** Gunicorn
- **Estáticos:** Whitenoise
- **Despliegue:** Docker (VPS con EasyPanel / DonWeb)

## Características principales

- **Registro rápido de observaciones** para docentes (uno o pocos toques)
- **Catálogo versionado** de 27 categorías de observación (positivas,
  neutras y de atención)
- **Control de acceso por roles**: docente, preceptor, directivo y admin
- **Visión transversal del alumno** reservada a roles autorizados
- **Solicitudes de información e intervenciones** institucionales
- **Auditoría inmutable** de todas las operaciones sensibles
- **Reportes por docente** para el equipo directivo

## Roles

| Rol | Alcance |
|-----|---------|
| Docente | Registra y consulta sus propias observaciones (sin DNI de alumnos) |
| Preceptor | Fichas, observaciones e intervenciones de su turno |
| Directivo | Visión transversal, reportes y administración de datos |
| Admin | Gestión técnica y de datos maestros |

## Documentación

- [Guía de despliegue en producción](docs/DESPLIEGUE.md)
- [Estado del proyecto](docs/ESTADO.md)
- Documentos de diseño en `ideas y conceptos/`

## Instalación local (desarrollo)

```bash
cd seguimiento_escolar
python -m venv venv
venv\Scripts\activate        # Windows (o source venv/bin/activate en Linux/Mac)
pip install -r requirements.txt

# Configurar .env (copiar .env.example y completar)
copy .env.example .env

# Crear base de datos PostgreSQL y aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar catálogo de observaciones
python manage.py loaddata catalogo_observaciones

# Ejecutar
python manage.py runserver
```

## Tests

```bash
python manage.py test --noinput
```

## Estado

Prototipo funcional en fase de prueba.
