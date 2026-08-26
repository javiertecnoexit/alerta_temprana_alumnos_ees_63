# Sistema de Seguimiento Escolar — Escuela Secundaria N.º 63
## Documento de revisión arquitectónica y preparación del desarrollo asistido por IA

**Versión:** 0.1  
**Institución objetivo:** Escuela Secundaria N.º 63  
**Ámbito:** Turno mañana y turno tarde  
**Tecnología base seleccionada:** Django + PostgreSQL + aplicación web responsive  
**Entorno de desarrollo:** Visual Studio Code  
**Agente implementador principal:** Cline  
**Agente supervisor y planificador:** OpenCode  

---

## 1. Propósito de este documento

Este documento está destinado principalmente a **OpenCode**.

OpenCode deberá utilizarlo junto con la documentación general del proyecto para:

1. revisar críticamente la arquitectura propuesta;
2. detectar ambigüedades, contradicciones, omisiones y riesgos;
3. proponer un modelo técnico coherente;
4. transformar los requisitos institucionales en especificaciones implementables;
5. preparar la documentación que deberá utilizar Cline;
6. generar prompts/tareas de desarrollo pequeños, verificables y ordenados;
7. definir qué pruebas deben acompañar cada funcionalidad;
8. identificar decisiones que todavía requieren resolución humana antes de programarlas.

**OpenCode no debe modificar el código del proyecto durante esta fase de revisión.**

Su función inicial es actuar como **arquitecto/revisor técnico y planificador**.

---

# 2. Contexto del proyecto

La Escuela Secundaria N.º 63 cuenta con estudiantes y docentes distribuidos en **dos turnos: mañana y tarde**.

El objetivo del sistema es disponer de una herramienta institucional que permita construir una visión más completa de la evolución de cada alumno mediante observaciones breves, estructuradas y contextualizadas, sin convertir el sistema en un simple libro de calificaciones.

El concepto central es:

> El profesor registra hechos observables de su propia actividad docente; el sistema organiza la información; los roles autorizados pueden analizarla transversalmente y tomar decisiones de acompañamiento.

El sistema deberá poder utilizarse inicialmente en una escala acotada y, si resulta exitoso, **adoptarse rápidamente por toda la escuela sin necesidad de rediseñar la arquitectura**.

Por este motivo, no se busca construir un prototipo descartable, sino una **primera versión institucional reducida, pero correctamente estructurada y preparada para crecer**.

---

# 3. Principios funcionales ya acordados

## 3.1. El alumno es la entidad central

El sistema debe organizar la información alrededor del alumno.

Un alumno puede tener:

- múltiples profesores;
- múltiples materias;
- múltiples observaciones;
- diferentes cursos a lo largo de su trayectoria;
- diferentes situaciones en distintos ciclos lectivos.

La historia previa del alumno no debe perderse cuando cambia de curso, división o ciclo lectivo.

---

## 3.2. El sistema no es principalmente un sistema de calificaciones

Las calificaciones son necesarias y podrán incorporarse, pero no constituyen el núcleo del proyecto.

El objetivo principal es registrar **señales y hechos observables** que puedan ayudar a detectar tempranamente cambios relevantes.

---

## 3.3. Registrar observaciones debe ser extremadamente rápido

La operación principal del profesor deberá poder realizarse en pocos segundos.

La interfaz debe priorizar:

- selección rápida de alumno;
- selección de categoría;
- un clic/toque para registrar;
- comentario opcional cuando sea necesario;
- mínimo ingreso manual de texto.

Se debe evitar exigir al docente una carga administrativa excesiva.

---

## 3.4. Las observaciones deben ser observables y estructuradas

Se debe evitar convertir la aplicación en un lugar para emitir diagnósticos o etiquetas subjetivas.

Preferir:

> “No completó la actividad propuesta.”

frente a:

> “Es irresponsable.”

La estructura deberá favorecer descripciones de conductas, participación, trabajo, convivencia, asistencia u otros fenómenos observables.

---

## 3.5. Deben registrarse eventos positivos y negativos

El sistema no debe enfocarse exclusivamente en problemas.

También debe permitir registrar:

- mejora significativa;
- participación destacada;
- compromiso;
- desempeño sobresaliente;
- iniciativa;
- colaboración;
- avances sostenidos;
- otras fortalezas observables.

El objetivo es que el sistema pueda ayudar a detectar tanto **necesidades de apoyo** como **fortalezas y oportunidades**.

Las señales positivas podrían servir posteriormente para orientar, entre otras posibilidades:

- becas;
- proyectos;
- olimpíadas;
- tutorías avanzadas;
- actividades extracurriculares;
- oportunidades institucionales.

---

## 3.6. Ausencia de reportes no equivale automáticamente a ausencia de problemas

El diseño debe distinguir, al menos conceptualmente, entre:

1. ausencia de señales relevantes;
2. ausencia de observaciones suficientes;
3. existencia de señales que justifican una revisión.

No debe interpretarse automáticamente:

> “No hay observaciones” = “todo está bien”.

---

# 4. Visibilidad y control de acceso

## 4.1. Principio general

Cada usuario debe acceder únicamente a la información necesaria para cumplir su función institucional.

Se debe aplicar el principio de **mínimo privilegio**.

---

## 4.2. Profesor

Un profesor podrá:

- iniciar sesión;
- ver los cursos/materias que tiene asignados;
- ver los alumnos correspondientes a dichas asignaciones;
- registrar observaciones relacionadas con su propia actividad docente;
- consultar sus propios registros cuando corresponda.

No deberá poder, por defecto:

- consultar observaciones de otros docentes;
- consultar una puntuación o clasificación global del alumno;
- consultar el conjunto de señales agregadas de otras materias;
- acceder a información que no corresponda a sus funciones.

---

## 4.3. Solicitud de información adicional

Puede contemplarse que un profesor solicite a un rol autorizado información sobre un alumno en particular.

La solicitud debe:

- quedar registrada;
- indicar quién la realizó;
- indicar cuándo fue realizada;
- permitir justificar el motivo;
- ser evaluada por el rol responsable de suministrar la información.

La respuesta no deberá convertirse en un mecanismo informal para evitar los permisos del sistema.

---

## 4.4. Preceptoría y directivos

Los roles autorizados deberán disponer de una visión más amplia del alumno, incluyendo la posibilidad de consultar información transversal según sus funciones.

La separación exacta entre preceptor, directivo y administrador debe ser definida en la especificación técnica y revisada institucionalmente.

---

## 4.5. Administrador

El administrador deberá gestionar la configuración institucional, usuarios, catálogos, relaciones académicas, ciclos lectivos y otros parámetros necesarios.

El rol de administrador técnico no debe confundirse automáticamente con el rol de autoridad pedagógica.

OpenCode deberá analizar esta separación y proponer una solución adecuada.

---

# 5. Contextualización de cada observación

Cada observación debe quedar asociada, como mínimo, a un contexto que permita saber:

- alumno;
- profesor que la registró;
- materia;
- curso/división;
- ciclo lectivo;
- fecha;
- hora;
- turno;
- categoría de observación;
- comentario opcional;
- estado del registro.

---

## 5.1. Relación con el horario docente

El sistema debe conocer las asignaciones docentes y, cuando corresponda, los horarios.

Al registrar una observación se debería poder determinar si el docente tenía efectivamente clase con ese grupo en ese momento.

Esto no necesariamente significa bloquear siempre un registro fuera de horario.

El sistema debe distinguir al menos entre:

- observación registrada dentro del horario previsto de clase;
- observación registrada fuera del horario previsto.

Las reglas exactas deben ser propuestas por OpenCode y posteriormente aprobadas.

---

# 6. Catálogo de observaciones

El sistema deberá contar con un catálogo estructurado de indicadores/observaciones.

Ejemplos iniciales, no definitivos:

### Participación

- participación activa;
- baja participación;
- ausencia de participación.

### Trabajo académico

- realiza las actividades;
- no completa la actividad;
- no entrega trabajo;
- dificultades persistentes;
- falta de materiales.

### Atención

- mantiene la atención;
- distracciones frecuentes;
- se queda dormido durante la clase.

### Comportamiento y convivencia

- interacción adecuada;
- conducta disruptiva;
- conflicto con pares;
- aislamiento observable;
- otra conducta relevante.

### Estado observable

Podría ser necesario contemplar indicadores tales como:

- apatía observable;
- tristeza observable;
- desmotivación observable;
- cambio significativo respecto del comportamiento habitual.

Estos indicadores deben diseñarse con especial cautela para evitar que el docente realice diagnósticos clínicos o psicológicos.

La descripción debe centrarse en lo observable.

Ejemplo preferible:

> “Se mostró notablemente callado y no participó durante la mayor parte de la clase.”

No:

> “Presenta depresión.”

### Evolución positiva

- mejora significativa;
- participación destacada;
- iniciativa;
- desempeño sobresaliente;
- compromiso destacado;
- colaboración con pares.

---

# 7. Extensibilidad del catálogo

Los directivos o administradores autorizados deberán poder incorporar nuevas categorías o indicadores cuando aparezcan necesidades institucionales.

Esto debe hacerse sin invalidar los registros históricos.

Por ello, el catálogo debe ser **versionable**.

Cada observación histórica debe conservar el significado de la categoría que existía cuando fue registrada.

No se debe permitir que modificar posteriormente el nombre de una categoría altere la interpretación histórica.

OpenCode deberá diseñar un mecanismo apropiado para:

- alta de categorías;
- baja lógica o desactivación;
- edición controlada;
- versionado;
- auditoría;
- compatibilidad con registros históricos.

---

# 8. Ciclo de vida de alumnos

El sistema debe contemplar:

- ingreso al comenzar el ciclo lectivo;
- ingreso durante el ciclo lectivo;
- baja durante el ciclo lectivo;
- cambio de curso/división;
- cambio de turno;
- egreso;
- promoción al año siguiente;
- repitencia, cuando corresponda;
- reincorporaciones u otras situaciones institucionales.

La baja no debe eliminar físicamente el historial del alumno.

Debe conservarse la trazabilidad de su permanencia en la institución.

---

# 9. Ciclo de vida de docentes

El sistema debe contemplar:

- alta de docente;
- asignación a materias/cursos;
- cambio de asignación;
- licencia;
- suplencia;
- finalización de suplencia;
- baja;
- cambios de turno o carga horaria.

Una suplencia debe ser temporal y estar asociada a un período válido.

Cuando finaliza una suplencia, el docente suplente debe perder el acceso correspondiente, pero sus registros históricos deben conservarse.

OpenCode deberá analizar cómo modelar esto sin sobrescribir la historia de asignaciones.

---

# 10. Ciclos lectivos y promoción

El sistema debe soportar múltiples ciclos lectivos.

Nunca se debe modificar el historial de un ciclo anterior para representar el nuevo ciclo.

La promoción debe modelarse como una nueva asignación del alumno a un curso/división dentro del nuevo ciclo lectivo.

El sistema debe permitir representar, entre otros casos:

- promoción de 2.º a 3.º;
- permanencia en el mismo año;
- cambio de división;
- cambio de turno;
- egreso;
- ingreso de nuevos alumnos.

El historial debe permitir reconstruir la trayectoria del alumno a lo largo de los años.

---

# 11. Visión institucional del alumno

Los roles autorizados podrán consultar una visión integrada del alumno.

Esta visión podrá combinar:

- evolución de observaciones;
- eventos positivos;
- asistencia, si se incorpora;
- calificaciones, si se incorpora;
- cambios de curso;
- intervenciones institucionales;
- tendencias temporales.

Sin embargo, la interfaz debe diferenciar claramente entre:

**datos observados** y **interpretaciones/indicadores derivados**.

El sistema no debe presentar una etiqueta como si fuera un diagnóstico.

---

# 12. Indicadores y alertas

Las alertas deberán interpretarse como **señales para revisión humana**, no como diagnósticos.

Ejemplos posibles:

- aumento de observaciones de una determinada categoría;
- señales provenientes de varias materias;
- cambio persistente respecto de períodos anteriores;
- combinación de asistencia, comportamiento y rendimiento;
- acumulación de fortalezas o desempeño destacado.

La mayoría de los alumnos podría no generar alertas y esto debe considerarse un comportamiento esperado del sistema.

OpenCode deberá estudiar cómo evitar falsos positivos y cómo representar la falta de información.

---

# 13. Intervenciones y seguimiento

Una alerta no debería cerrar el proceso.

Los roles autorizados deberán poder registrar acciones posteriores, por ejemplo:

- entrevista;
- contacto con familia/tutor, cuando corresponda;
- seguimiento pedagógico;
- derivación institucional;
- acompañamiento;
- propuesta de actividad especial;
- acceso a proyecto/beca/oportunidad;
- cierre de seguimiento.

Esto permitiría pasar de un modelo de “detectar problemas” a un modelo de **detectar, intervenir y hacer seguimiento**.

---

# 14. Auditoría y trazabilidad

Los registros relevantes deben conservar:

- usuario que creó el registro;
- fecha y hora;
- contexto de la acción;
- cambios posteriores;
- usuario que realizó un cambio;
- fecha y hora del cambio;
- motivo cuando corresponda.

La eliminación física de datos sensibles debe ser excepcional y gobernada por políticas claras.

OpenCode deberá proponer un esquema de auditoría técnicamente razonable para Django/PostgreSQL.

---

# 15. Seguridad

La seguridad es un requisito del núcleo del sistema, no una etapa final.

Debe contemplarse al menos:

- autenticación segura;
- control de autorización por rol;
- control de autorización por asignación concreta;
- protección contra acceso horizontal no autorizado;
- protección CSRF;
- validación del lado servidor;
- gestión segura de sesiones;
- HTTPS en producción;
- política de contraseñas o integración con identidad institucional, si se adopta;
- registro de eventos de seguridad relevantes;
- copias de seguridad;
- recuperación ante fallos;
- separación de desarrollo, pruebas y producción;
- protección de datos reales durante el desarrollo.

OpenCode deberá identificar amenazas específicas del dominio escolar.

---

# 16. Arquitectura técnica inicial

## 16.1. Stack elegido

### Backend

- Python
- Django

### Base de datos

- PostgreSQL

### Frontend inicial

- Django Templates
- HTML
- CSS
- JavaScript donde sea necesario

No se incorporará React u otro framework de frontend complejo salvo que exista una necesidad justificada.

### Herramientas de desarrollo

- Visual Studio Code
- Git
- Cline
- OpenCode

### Despliegue

La arquitectura deberá poder evolucionar desde un entorno de desarrollo local hacia un entorno de producción institucional sin rediseñar el dominio.

---

# 17. Enfoque de arquitectura

Para la primera etapa se prefiere un **monolito modular bien estructurado** antes que una arquitectura distribuida o basada en microservicios.

El sistema podría organizarse aproximadamente en aplicaciones Django separadas por dominio, por ejemplo:

```text
usuarios/
alumnos/
docentes/
cursos/
materias/
horarios/
ciclos_lectivos/
observaciones/
seguimiento/
reportes/
auditoria/
```

La división definitiva deberá ser propuesta por OpenCode.

---

# 18. Escalabilidad

Aunque el alcance inicial sea solamente la Escuela Secundaria N.º 63, la arquitectura deberá soportar sin rediseño fundamental:

- todos los docentes del turno mañana;
- todos los docentes del turno tarde;
- equipos directivos y preceptoría;
- todos los alumnos de la escuela;
- múltiples cursos y divisiones;
- varios ciclos lectivos históricos;
- crecimiento de observaciones a lo largo de los años.

No se debe optimizar para una cantidad artificialmente pequeña de usuarios.

Tampoco se debe sobrediseñar prematuramente.

OpenCode deberá proponer un equilibrio razonable entre simplicidad y capacidad de crecimiento.

---

# 19. Desarrollo asistido por agentes

## 19.1. Rol de Cline

Cline será el principal agente de implementación.

Podrá encargarse de:

- crear/modificar código;
- crear modelos Django;
- crear migrations;
- implementar vistas y formularios;
- implementar lógica de negocio;
- crear interfaces;
- escribir tests;
- ejecutar tests;
- corregir errores según especificaciones.

Cline deberá trabajar sobre tareas acotadas y verificables.

---

## 19.2. Rol de OpenCode

OpenCode actuará como:

- revisor de arquitectura;
- analista del dominio;
- generador de especificaciones técnicas;
- revisor de seguridad;
- revisor de tests;
- planificador de tareas;
- segunda opinión técnica.

En esta fase inicial, OpenCode **no debe modificar el código**.

---

# 20. Proceso obligatorio de trabajo entre agentes

Se propone el siguiente flujo:

```text
REQUISITO
   ↓
ANÁLISIS DE OPENCODE
   ↓
ESPECIFICACIÓN TÉCNICA
   ↓
TAREA/PROMPT PARA CLINE
   ↓
IMPLEMENTACIÓN DE CLINE
   ↓
TESTS
   ↓
REVISIÓN DE OPENCODE
   ↓
CORRECCIONES
   ↓
REVISIÓN HUMANA
   ↓
COMMIT / MERGE
```

Cline y OpenCode no deberían modificar simultáneamente los mismos archivos.

---

# 21. Requisitos para los prompts que OpenCode genere para Cline

Cada prompt debe ser:

- autocontenido;
- específico;
- limitado a una funcionalidad coherente;
- basado en la documentación del proyecto;
- explícito respecto de los archivos que puede modificar cuando corresponda;
- explícito respecto de los archivos que no debe modificar cuando corresponda;
- acompañado de criterios de aceptación;
- acompañado de pruebas requeridas;
- acompañado de restricciones de seguridad;
- acompañado de condiciones de finalización.

Los prompts no deben contener instrucciones ambiguas como:

> “Mejorá el sistema.”

Deben contener instrucciones verificables como:

> “Implementá el permiso que impide a un docente consultar observaciones creadas por otro docente. Agregá pruebas de autorización para acceso permitido y denegado.”

---

# 22. Formato recomendado para cada tarea de Cline

OpenCode deberá generar cada tarea utilizando, como mínimo, esta estructura:

```text
TÍTULO

OBJETIVO

CONTEXTO

DOCUMENTACIÓN RELEVANTE

ALCANCE

NO INCLUIR

CAMBIOS ESPERADOS

REGLAS DE NEGOCIO

SEGURIDAD Y PERMISOS

CRITERIOS DE ACEPTACIÓN

TESTS OBLIGATORIOS

COMANDOS DE VERIFICACIÓN

CONDICIÓN DE FINALIZACIÓN
```

---

# 23. Tests y Definition of Done

Una tarea solo se considera terminada cuando:

```text
[ ] Implementación realizada
[ ] Tests creados o actualizados
[ ] Tests pasan
[ ] Reglas de negocio verificadas
[ ] Permisos verificados
[ ] No existen accesos no autorizados conocidos
[ ] Migraciones verificadas
[ ] Documentación actualizada cuando corresponde
[ ] OpenCode revisó el cambio
[ ] Revisión humana realizada
[ ] Commit realizado
```

---

# 24. Primera fase que OpenCode debe planificar

OpenCode debe preparar una secuencia de trabajo empezando por infraestructura y dominio, no por pantallas finales.

Orden conceptual esperado:

1. estructura del repositorio;
2. entorno Python;
3. Django;
4. PostgreSQL;
5. configuración base;
6. usuarios y autenticación;
7. roles y permisos;
8. ciclo lectivo;
9. alumnos;
10. cursos/divisiones y turnos;
11. profesores;
12. materias;
13. asignaciones profesor-materia-curso;
14. horarios;
15. suplencias;
16. catálogo versionado de observaciones;
17. registro de observaciones;
18. auditoría;
19. paneles de consulta;
20. indicadores y seguimiento;
21. intervenciones;
22. funcionalidades de cierre y apertura de ciclo.

OpenCode puede modificar este orden si encuentra una dependencia técnica o conceptual que lo justifique, pero debe explicar el motivo.

---

# 25. Datos reales y entorno de prueba

Nunca se deben utilizar datos personales reales de alumnos o docentes en el desarrollo local de los agentes salvo autorización institucional explícita y un diseño de protección apropiado.

Se deberán utilizar datos ficticios para:

- desarrollo;
- pruebas;
- demostraciones;
- validación automatizada.

La producción deberá ser un entorno separado.

---

# 26. Cuestiones que OpenCode debe investigar o dejar explícitamente abiertas

Antes de generar la versión definitiva de prompts para Cline, OpenCode deberá identificar cualquier cuestión pendiente, especialmente:

- granularidad de roles;
- separación entre administración técnica y autoridad institucional;
- permisos exactos de preceptoría;
- reglas para registros fuera de horario;
- posibilidad y condiciones de edición de observaciones;
- política de corrección y auditoría;
- tratamiento de categorías sensibles;
- retención de datos;
- backups y recuperación;
- autenticación institucional;
- reglas de cierre de ciclo lectivo;
- política de altas y bajas;
- política de suplencias;
- reglas para indicadores y alertas;
- tratamiento de información positiva;
- requisitos legales y regulatorios aplicables en Argentina y en la jurisdicción educativa correspondiente.

Si una decisión no puede resolverse de forma segura, OpenCode deberá marcarla como **DECISIÓN HUMANA REQUERIDA** y no inventar una política.

---

# 27. Entregables que debe producir OpenCode después de revisar este documento

La salida esperada de OpenCode deberá incluir al menos:

## A. Informe de revisión arquitectónica

Debe señalar:

- inconsistencias;
- riesgos;
- dependencias;
- decisiones pendientes;
- mejoras propuestas;
- riesgos de seguridad;
- riesgos de privacidad;
- riesgos de calidad de datos.

## B. Modelo de dominio propuesto

Debe definir las entidades, relaciones, cardinalidades y principales restricciones.

## C. Modelo de autorización

Debe definir qué roles pueden hacer qué acciones sobre qué objetos.

## D. Arquitectura Django propuesta

Debe proponer las aplicaciones/módulos, modelos principales y límites entre componentes.

## E. Estrategia de tests

Debe indicar qué reglas requieren tests de unidad, integración y autorización.

## F. Plan de desarrollo

Debe ordenar las tareas y dependencias.

## G. Documentación para Cline

Debe crear las especificaciones necesarias para implementar cada módulo.

## H. Prompts para Cline

Debe generar prompts/tareas consecutivos, pequeños y verificables.

---

# 28. Criterio de calidad para la salida de OpenCode

No se considerará suficiente que OpenCode produzca una lista genérica de tareas.

La planificación deberá demostrar que comprendió específicamente:

- la Escuela Secundaria N.º 63;
- sus dos turnos;
- el alumno como entidad central;
- la relación entre profesores, materias y cursos;
- el acceso restringido del docente a su propio ámbito;
- la visión transversal reservada a roles autorizados;
- la necesidad de minimizar sesgos;
- el registro rápido de observaciones;
- la coexistencia de señales negativas y positivas;
- las altas y bajas de alumnos;
- las altas, bajas y suplencias docentes;
- los cambios entre ciclos lectivos;
- la conservación del historial;
- la trazabilidad de cada evento;
- la necesidad de poder crecer rápidamente a toda la institución.

---

# 29. Regla final para OpenCode

**No inventar funcionalidades por iniciativa propia cuando afecten políticas institucionales.**

**No modificar el código durante esta etapa de análisis.**

**No convertir decisiones pedagógicas o institucionales en reglas automáticas sin justificación.**

**No generar una arquitectura más compleja de la necesaria.**

**No reducir el proyecto a un CRUD de alumnos.**

**No tratar una alerta como un diagnóstico.**

La prioridad es producir una base técnica clara, segura, mantenible y comprensible, que permita a Cline implementar el sistema de manera incremental y verificable.

---

# 30. Resultado esperado de esta etapa

Al finalizar la revisión, deberá existir un conjunto coherente de documentos que permita iniciar el desarrollo real en Visual Studio Code sin depender de la conversación original.

El flujo esperado es:

```text
DOCUMENTACIÓN DEL PROYECTO
          ↓
       OPENCODE
          ↓
REVISIÓN + ARQUITECTURA
          ↓
ESPECIFICACIONES TÉCNICAS
          ↓
PROMPTS / TAREAS CLINE
          ↓
       CLINE
          ↓
IMPLEMENTACIÓN + TESTS
          ↓
       OPENCODE
          ↓
     REVISIÓN
          ↓
     NOSOTROS
          ↓
     ACEPTACIÓN
```

Este documento constituye la **base de trabajo para la fase de revisión y planificación técnica previa a la implementación**.
