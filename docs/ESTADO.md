# Estado del proyecto — ES63

**Fecha:** 26/08/2026
**Último commit:** 3dc176d (A + B + C1 + datos demo)

## Stack
- Django 4.2 + PostgreSQL
- 9 apps: usuarios, ciclos_lectivos, estructura_escolar, alumnos,
  observaciones, asistencia, auditoria, seguimiento, administracion

## Fase 2 de mejoras — progreso

### Tarea A — Ocultar DNI al docente ✅ COMPLETA
- El docente ya no ve DNI en la lista de alumnos
- El directivo y preceptor SÍ lo ven

### Tarea B — Ampliar rol del preceptor ✅ COMPLETA
- Campo `materia` opcional en `Observacion` (observaciones preceptoriales)
- El preceptor puede: ver ficha de su turno, registrar observaciones
  (sin materia), registrar intervenciones — SIEMPRE limitado a su turno
- Helper `_preceptor_puede_ver_alumno` y `_alumno_del_turno_preceptor`
- Decorador `directivo_o_preceptor` en `apps/usuarios/decorators.py`

### Tarea C — App administracion (EN PROGRESO)
- **C1 ✅ COMPLETA**: app `administracion` creada, helper
  `registrar_auditoria` (activa el AuditLog), panel índice,
  decorador `directivo_o_admin`
- **C2 ⏳ PENDIENTE**: CRUD de Alumno + Docente (alta/baja/edición +
  asignación) con auditoría y confirmación
- **C3 ⏳ PENDIENTE**: CRUD de Materia, Curso, Turno, CicloLectivo
- **C4 ⏳ PENDIENTE**: CRUD de Horario y AsignacionDocente

### Tarea D — Reportes por profesor ⏳ PENDIENTE
- Panel de participación (obs por docente en período)
- Filtro de alumnos por docente
- Filtro de docentes por curso
- Estilo de reporte por docente (distribución positivo/neutro/atención)
- Ficha de alumno filtrada por docente+curso

## Decisiones acordadas
- Preceptor: NO carga datos maestros (solo consulta); sí reportes igual
  que directivo (limitado a su turno)
- Carga de datos maestros: directivo + admin (interfaces propias con
  aviso de confirmación y auditoría de cada intervención)
- C2/C3/C4 usan el helper `registrar_auditoria` de administracion

## Próximos pasos
1. Terminar C2 (CRUD Alumno + Docente)
2. C3 (Materia, Curso, Turno, CicloLectivo)
3. C4 (Horario y AsignacionDocente)
4. D (reportes por profesor)

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
