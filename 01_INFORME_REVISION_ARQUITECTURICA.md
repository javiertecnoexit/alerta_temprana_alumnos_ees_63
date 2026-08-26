# Informe de Revisión Arquitectónica
## Sistema de Seguimiento Temprano - Escuela Secundaria N.º 63
**Versión:** 1.0 | **Fecha:** 25 de agosto de 2026 | **Fase:** Pre-implementación

---

## 1. Resumen Ejecutivo

La documentación existente (documento base v0.2, proyecto ES63 v0.3, guía OpenCode/Cline v0.1) proporciona una base conceptual **sólida y coherente** para iniciar la implementación. Las decisiones fundamentales están tomadas y alineadas: tecnología (Django + PostgreSQL), arquitectura (monolito modular), principios de dominio (alumno central, separación de roles, catálogo versionado, historial preservado).

El proyecto está listo para pasar a especificación técnica detallada y generación de prompts para Cline.

---

## 2. Fortalezas Identificadas

| Área | Fortaleza |
|------|-----------|
| **Dominio** | Principios claros: alumno central, hechos observables, no diagnósticos, registro rápido, eventos positivos/negativos |
| **Roles y permisos** | Separación estricta docente/directivo, principio de mínimo privilegio, solicitudes auditadas |
| **Ciclo de vida** | Modelo histórico para alumnos, docentes, cursos, ciclos lectivos, suplencias - sin pérdida de historial |
| **Catálogo** | Versionado, controlado institucionalmente, desactivación en lugar de borrado |
| **Tecnología** | Stack maduro (Django/PostgreSQL), web responsive, sin over-engineering inicial |
| **Seguridad/Privacidad** | Considerada desde el diseño, no como capa final |
| **Escalabilidad** | Arquitectura preparada para adopción institucional completa |

---

## 3. Inconsistencias y Ambigüedades Detectadas

### 3.1. Roles: Preceptor vs Directivo vs Administrador Institucional
- **Documento base** (secc 5.2): "Preceptor / personal autorizado" - alcance por definir según organización
- **Proyecto ES63** (secc 11.1): Roles separados: Preceptor, Equipo directivo, Administrador institucional, Administrador técnico
- **Guía** (secc 4.4): "Separación exacta entre preceptor, directivo y administrador debe definirse en especificación técnica"
- **Riesgo**: Permisos mal definidos → acceso indebido o bloqueo de funciones necesarias
- **Acción requerida**: Definir matriz de permisos granular antes de implementar authz

### 3.2. Registro fuera de horario
- **Documento base** (secc 8): "No necesariamente impedir el registro... contexto horario debe quedar guardado"
- **Proyecto ES63** (secc 10.1): "Podrá requerir un nivel adicional de justificación según reglas institucionales"
- **Guía** (secc 5.1): "Reglas exactas deben ser propuestas por OpenCode y posteriormente aprobadas"
- **Decisión pendiente**: ¿Bloquear? ¿Permitir con justificación obligatoria? ¿Solo warn?

### 3.3. Edición/borrado de observaciones
- **Documento base** (secc 4.7): Trazabilidad de modificaciones
- **Proyecto ES63**: No especifica política de corrección
- **Guía** (secc 26): "Posibilidad y condiciones de edición de observaciones", "Política de corrección y auditoría"
- **Riesgo**: Sin política clara → integridad de datos comprometida o rigidez excesiva

### 3.4. Categorías "Estado observable" (emocionales)
- **Documento base** (secc 9): Incluye "tristeza", "aislamiento", "apatía" como observables
- **Proyecto ES63** (secc 7.1): "Inclusión de categorías relacionadas con estado emocional deberá definirse con especial cuidado"
- **Guía** (secc 6): Lista "apatía observable", "tristeza observable", "desmotivación observable" con cautela
- **Riesgo**: Deriva hacia pseudo-diagnóstico clínico
- **Acción**: Requerir validación pedagógica/legal antes de incluir en catálogo inicial

### 3.5. Asistencia
- **Documento base** (secc 12): "Primera etapa... al menos ser capaz de almacenar y eventualmente relacionar"
- **Proyecto ES63** (secc 25): "Integración de asistencia" como evolución posterior
- **Guía**: No menciona asistencia en MVP
- **Inconsistencia**: ¿Está en MVP o no? Documento base sugiere sí (básico), Proyecto ES63 dice no.

### 3.6. Calificaciones
- **Documento base** (secc 11): "Podrán incorporarse como una de las familias de información"
- **Proyecto ES63** (secc 25): "Integración más completa de calificaciones" como evolución posterior
- **Guía** (secc 3.2): "No es principalmente un sistema de calificaciones... podrán incorporarse"
- **Aclaración necesaria**: ¿MVP incluye modelo de calificaciones básico o solo placeholder?

### 3.7. Separación Administrador Técnico vs Institucional
- **Proyecto ES63** (secc 11.1): "Separación entre administrador institucional y administrador técnico deberá evaluarse"
- **Guía** (secc 4.5): "OpenCode deberá analizar esta separación y proponer una solución adecuada"
- **Decisión pendiente**: ¿Un rol "admin" con permisos técnicos + flag? ¿Dos roles distintos?

---

## 4. Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| **Modelo de datos subóptimo para consultas transversales** | Media | Alto | Diseñar ER con índices y vistas materializadas para panel directivo desde el inicio |
| **Permisos por asignación (object-level) complejos en Django** | Alta | Alto | Usar `django-guardian` o policies custom desde el inicio; no improvisar en vistas |
| **Historial de catálogo versionado** | Media | Medio | Implementar `ObservationCatalog` con `valid_from`/`valid_to` y FK a versión en `Observation` |
| **Suplencias solapadas / transiciones** | Media | Alto | Modelo `TeacherAssignment` con fechas, tipo (titular/suplente), `replaces` FK auto-referencial |
| **Cierre de ciclo lectivo masivo** | Baja | Alto | Management command transaccional para promoción masiva + validaciones previas |
| **Falsos positivos en alertas** | Alta | Medio | Reglas configurables, umbrales por ciclo/turno/materia, revisión humana obligatoria |
| **Datos reales en desarrollo** | Media | Crítico | Seeds/fixtures con datos sintéticos; `.env` para credenciales; nunca volcar BD real |

---

## 5. Riesgos de Privacidad y Legalidad (Argentina)

| Tema | Consideración |
|------|---------------|
| **Ley 25.326 (Protección Datos Personales)** | Consentimiento, finalidad, seguridad, acceso, rectificación, supresión |
| **Ley 26.061 (Protección Integral Niños/Adolescentes)** | Interés superior, participación, confidencialidad |
| **Normativa educativa provincial/jurisdiccional** | Revisar antes de producción: quien accede a qué, retención, cesión de datos |
| **Menores de edad** | Datos sensibles (salud, comportamiento) → mayor protección |
| **Retención** | Definir plazos: observaciones (¿5 años post-egreso?), auditoría (¿inalterable?) |
| **Acceso técnico** | Admin técnico NO ve datos pedagógicos sin auditoría; logs de acceso |

**Acción**: Requerir revisión legal formal antes de poner en producción con datos reales.

---

## 6. Riesgos de Calidad de Datos

| Riesgo | Descripción | Mitigación |
|--------|-------------|------------|
| **Sesgo de reporte** | Docentes reportan solo negativos / solo algunos alumnos | UI que sugiere positivos, métricas de cobertura por docente |
| **Inconsistencia inter-observador** | "Baja participación" significa cosas distintas | Definiciones obligatorias en catálogo, ejemplos, capacitación |
| **Sub-reporte** | Docentes no usan el sistema | Registro < 10 seg, recordatorios contextuales, valor percibido |
| **Datos fantasmas** | Alumnos sin observaciones = "todo bien" | Distinguir explícitamente "sin señales" vs "sin datos" en UI y alertas |
| **Catálogo inflado** | Demasiadas categorías → ruido | Proceso controlado de alta, revisión periódica, métricas de uso |

---

## 7. Decisiones Pendientes (Requieren Resolución Humana)

| # | Decisión | Impacto | Urgencia |
|---|----------|---------|----------|
| 1 | Matriz exacta de permisos Preceptor/Directivo/AdminInstitucional | Authz core | **Antes de iniciar auth** |
| 2 | Política: registro fuera de horario (bloquear/warn/justificar) | UX docente, calidad dato | **Antes de módulo observaciones** |
| 3 | Política: edición/borrado observaciones (ventana temporal, roles, auditoría) | Integridad, confianza | **Antes de módulo observaciones** |
| 4 | Catálogo inicial definitivo (validar categorías emocionales) | Calidad dato, legal | **Antes de seeding catálogo** |
| 5 | ¿Asistencia en MVP? (modelo básico vs solo placeholder) | Alcance MVP | **Antes de planificar sprints** |
| 6 | ¿Calificaciones en MVP? (modelo básico vs solo placeholder) | Alcance MVP | **Antes de planificar sprints** |
| 7 | Separación Admin Técnico vs Institucional (roles, permisos) | Seguridad, auditoría | **Antes de módulo usuarios** |
| 8 | Reglas de alertas: umbrales, ventanas temporales, combinaciones | Motor indicadores | **Antes de fase indicadores** |
| 9 | Retención de datos por tipo (observaciones, auditoría, auth logs) | Legal, storage | **Antes de producción** |
| 10 | Autenticación: local vs SSO institucional (Google/Microsoft/SAML) | Infra, onboarding | **Antes de despliegue** |

---

## 8. Mejoras Propuestas a la Arquitectura

### 7.1. Añadir app `core` transversal
```
core/
  models.py      # AbstractBaseModel (created_at, updated_at, created_by, updated_by)
  permissions.py # BasePermission classes, mixins
  utils.py       # Helpers transversales
  middleware.py  # Request context (current_teacher_assignment, etc.)
```

### 7.2. Separar `observations` en dos apps
```
observations/
  catalog/       # ObservationCategory, CategoryVersion, Definition
  registry/      # Observation, Comment, validation, signals
```
Razón: Catálogo cambia poco, registro es alta frecuencia. Ciclos de vida y permisos distintos.

### 7.3. App `academic` para estructura escolar
```
academic/
  models: Cycle, Turn, Course, Division, Subject, Schedule
  managers: QuerySets con filtros por ciclo activo, turno, etc.
```

### 7.4. App `people` unificada
```
people/
  models: Person (abstract), Student, Teacher, Guardian
  assignments: StudentEnrollment, TeacherAssignment
```
Evita duplicar lógica de persona, historial, contactos.

### 7.5. App `tracking` para visión directiva
```
tracking/
  models: Alert, Intervention, FollowUp, InformationRequest
  services: IndicatorEngine, AlertGenerator (tasks/management commands)
  views: Dashboards, student_detail, reports
```
Separación clara: `observations.registry` = escritura docente; `tracking` = lectura/autorizado.

---

## 9. Dependencias Críticas entre Módulos

```
┌─────────────────┐
│  core (base)    │ ◄── Primero: modelos abstractos, permissions, utils
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌─────────┐
│ people│ │ academic│ ◄── Segundo: personas, estructura escolar, ciclos
└───┬───┘ └────┬────┘
    │          │
    └────┬─────┘
         ▼
┌─────────────────┐
│ assignments     │ ◄── Tercero: TeacherAssignment, StudentEnrollment (con fechas)
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────────┐
│catalog │ │ registry   │ ◄── Cuarto: catálogo versionado + registro observaciones
└────────┘ └─────┬──────┘
                 │
                 ▼
         ┌───────────────┐
         │  tracking     │ ◄── Quinto: alertas, intervenciones, panel directivo
         └───────────────┘
```

---

## 10. Conclusión y Próximos Pasos

La documentación está **suficientemente madura** para proceder a especificación técnica. Los riesgos identificados son manejables con decisiones explícitas (sección 7) antes de los puntos de no retorno en la implementación.

**Orden recomendado de trabajo inmediato:**
1. Resolver decisiones pendientes #1, #2, #3, #7 (authz, horario, edición, admin roles)
2. Producir Modelo de Dominio (ER) formal
3. Producir Matriz de Permisos formal
4. Definir Arquitectura Django (apps, modelos, managers, signals)
5. Generar especificaciones por módulo + prompts para Cline

---

**Firmado:** OpenCode (Arquitecto/Planificador)
**Fecha:** 25/08/2026