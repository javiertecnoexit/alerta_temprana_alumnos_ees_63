# Estado del proyecto — ES63

**Fecha:** 26/08/2026
**Último commit:** 3dc176d (A + B + C1 + datos demo)

## Stack
- Django 4.2 + PostgreSQL
- 9 apps: usuarios, ciclos_lectivos, estructura_escolar, alumnos,
  observaciones, asistencia, auditoria, seguimiento, administracion

## Fase 2 de mejoras — COMPLETA ✅

### Tarea A — Ocultar DNI al docente ✅
- El docente ya no ve DNI en la lista de alumnos
- El directivo y preceptor SÍ lo ven

### Tarea B — Ampliar rol del preceptor ✅
- Campo `materia` opcional en `Observacion` (observaciones preceptoriales)
- El preceptor puede: ver ficha de su turno, registrar observaciones
  (sin materia), registrar intervenciones — SIEMPRE limitado a su turno
- Helper `_preceptor_puede_ver_alumno` y `_alumno_del_turno_preceptor`
- Decorador `directivo_o_preceptor` en `apps/usuarios/decorators.py`

### Tarea C — App administracion ✅
- C1: app creada + helper `registrar_auditoria` (activa AuditLog) +
  panel índice + decorador `directivo_o_admin`
- C2: CRUD de Alumno + Docente con confirmación y auditoría
- C3: CRUD de Materia, Turno, Curso, CicloLectivo
- C4: CRUD de AsignacionDocente y Horario (eliminación auditada)
- Patrón de 2 pasos: formulario → sesión → confirmación → guardar
- Auditoría (crear/modificar/eliminar) en cada acción

### Tarea D — Reportes por profesor ✅
- Panel de participación (obs por docente en período)
- Filtro de alumnos por docente
- Filtro de docentes por curso
- Estilo de reporte por docente (distribución positivo/neutro/atención
  y por familia)
- Ficha de alumno filtrada por docente+curso
- Preceptor restringido a su turno en todos los reportes

## Decisiones acordadas
- Preceptor: NO carga datos maestros (solo consulta); sí reportes igual
  que directivo (limitado a su turno)
- Carga de datos maestros: directivo + admin (interfaces propias con
  aviso de confirmación y auditoría de cada intervención)

## Estado: Fase 2 de mejoras COMPLETA
Todas las tareas (A, B, C1-C4, D) terminadas, verificadas y commiteadas.

## Credenciales demo
- admin / Admin1327! (superusuario)
- docente_mat, docente_leng, docente_hist, preceptor_manana,
  preceptor_tarde, directivo1, admin_demo / Demo1234

## Comandos útiles
```
cd seguimiento_escolar
..\venv\Scripts\python.exe manage.py runserver
..\venv\Scripts\python.exe manage.py test --noinput
..\venv\Scripts\python.exe manage.py seed_demo
```
