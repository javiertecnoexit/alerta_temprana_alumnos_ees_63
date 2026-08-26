# Sistema de Seguimiento Temprano del Alumno

**Documento base de orientación para el desarrollo — Versión 0.2**  
**Fecha:** 24 de agosto de 2026

---

## 1. Propósito del proyecto

El proyecto propone desarrollar un sistema digital institucional orientado al **seguimiento temprano e integral de los alumnos de una escuela secundaria**.

La finalidad principal no es reemplazar el sistema de calificaciones ni convertir la aplicación en un libro de notas digital. El propósito es permitir que los docentes registren, de manera **simple, rápida y estructurada**, situaciones observables durante sus clases, de modo que el equipo directivo pueda detectar cambios o patrones que difícilmente serían visibles desde una sola materia.

La idea central es:

> **Cada docente aporta una observación parcial del alumno; el sistema permite al equipo autorizado construir una visión transversal y detectar tempranamente señales que podrían requerir seguimiento.**

El sistema debe ayudar a que la institución pueda intervenir antes de esperar exclusivamente al cierre de notas o a que el problema se vuelva evidente.

---

## 2. Problema que se busca resolver

Un alumno tiene contacto con numerosos profesores durante la semana. Cada docente observa solamente una parte de su desempeño y comportamiento.

En la práctica, la información relevante suele quedar distribuida entre conversaciones informales, mensajes, reuniones, recuerdos personales y registros aislados.

Esto genera varias dificultades:

- un profesor puede desconocer que otros docentes están observando cambios similares;
- la comunicación entre docentes depende de que alguien tome la iniciativa de comunicarse;
- algunas situaciones se detectan recién cuando repercuten en las calificaciones;
- las observaciones informales pueden perderse o no quedar registradas;
- el equipo directivo puede recibir información fragmentada y tardía;
- no existe necesariamente una visión temporal y transversal del alumno.

El sistema busca transformar esas observaciones dispersas en **datos estructurados, contextualizados y trazables**, sin quitar al equipo educativo la responsabilidad de interpretar la situación.

---

## 3. Fundamento conceptual

El proyecto se alinea conceptualmente con los **sistemas de alerta temprana (Early Warning Systems)** utilizados en educación.

Estos sistemas suelen trabajar con tres grandes familias de indicadores:

1. **Asistencia**
2. **Comportamiento / compromiso escolar**
3. **Desempeño académico**

La literatura sobre estos sistemas también destaca que los indicadores y sus umbrales deben analizarse y adaptarse al contexto concreto de cada institución, en lugar de copiar reglas universales. Asimismo, las alertas deben servir para orientar el seguimiento y la intervención, y no convertirse en diagnósticos o etiquetas permanentes sobre los alumnos.

Fuentes de referencia iniciales:

- Institute of Education Sciences (IES), recursos sobre Early Warning Systems.
- Regional Educational Laboratory (REL), recursos sobre indicadores de alerta temprana.
- U.S. Department of Education / Student Privacy, principios de acceso y protección de datos educativos.

> **Nota:** Estas referencias sirven como punto de partida conceptual. Antes de una implementación real deberán revisarse la normativa argentina y las políticas de la jurisdicción educativa correspondiente.

---

## 4. Principios de diseño

El sistema deberá desarrollarse siguiendo los siguientes principios.

### 4.1. El alumno es la entidad central

La aplicación no debe organizarse principalmente alrededor de las notas o de los profesores. El objeto central del sistema es el **alumno y su evolución a lo largo del tiempo**.

Cada profesor aporta información sobre ese alumno desde el contexto de su propia materia.

### 4.2. Registrar observaciones, no etiquetar alumnos

El docente debe registrar **conductas o situaciones observables**, evitando transformar una percepción subjetiva en una clasificación del alumno.

Ejemplo preferido:

> "No completó la actividad propuesta."

En lugar de:

> "Es irresponsable."

### 4.3. Catálogo institucional de observaciones, extensible y controlado

Las categorías de observación no deben quedar completamente abiertas a cada docente. Debe existir un **catálogo institucional controlado** que permita mantener consistencia entre profesores y, al mismo tiempo, evolucionar cuando aparezcan nuevas necesidades.

El catálogo podrá ser ampliado por usuarios con permisos de administración institucional o directiva. Por ejemplo, además de las categorías iniciales previstas, la institución podría incorporar indicadores como:

- apatía o falta persistente de iniciativa;
- somnolencia o quedarse dormido durante la clase;
- tristeza o cambio emocional observable;
- aislamiento;
- aumento de participación;
- liderazgo positivo;
- mejora notable del desempeño;
- interés excepcional por una temática;
- colaboración con compañeros;
- otras conductas relevantes definidas institucionalmente.

Cada nueva categoría deberá incluir una **definición y criterio de uso** para reducir interpretaciones diferentes entre docentes. El objetivo no es registrar diagnósticos clínicos o personales, sino situaciones observables y pedagógicamente relevantes. Por ejemplo, puede registrarse "se quedó dormido durante la clase" como hecho observable, pero no "presenta depresión" o "tiene un problema psicológico".

El sistema deberá conservar la versión del catálogo utilizada en cada registro, de modo que un cambio posterior de las categorías no altere la interpretación histórica de los datos.

La aplicación debe favorecer descripciones concretas y evitar diagnósticos informales.

### 4.3. Registro rápido

Registrar una observación debe requerir el mínimo esfuerzo posible.

La acción principal debería poder realizarse con **uno o pocos toques**.

El comentario libre será opcional en la mayoría de las situaciones y se utilizará especialmente cuando la categoría estructurada no sea suficiente.

### 4.4. Información mínima necesaria

Cada usuario debe ver solamente la información necesaria para cumplir su función.

Esto reduce riesgos de privacidad, sesgos y usos indebidos de la información.

### 4.5. Separar observación de interpretación

El profesor aporta observaciones.

El sistema organiza y agrega datos.

El equipo autorizado interpreta el conjunto y decide las intervenciones.

El sistema **no debe convertir automáticamente una señal en un diagnóstico del alumno**.

### 4.6. Contextualización

Toda observación debe conservar su contexto:

- alumno;
- profesor;
- materia;
- curso/división;
- fecha;
- hora;
- relación del docente con ese alumno;
- contexto horario de la clase.

### 4.7. Trazabilidad

Las acciones importantes deben quedar registradas.

Debe ser posible saber, como mínimo:

- quién creó un registro;
- cuándo lo creó;
- qué información registró;
- si posteriormente fue modificado;
- quién realizó la modificación;
- cuándo ocurrió.

### 4.8. Evolución antes que fotografía aislada

Un evento aislado no necesariamente indica un problema.

El sistema debe permitir observar **frecuencia, recencia y tendencia** a lo largo del tiempo.

---

## 5. Roles de usuario

Se propone inicialmente un sistema de acceso basado en roles.

### 5.1. Profesor

Puede:

- acceder a sus cursos asignados;
- acceder a los alumnos que corresponden a sus materias;
- registrar observaciones relativas a su propia actividad docente;
- consultar sus propios registros;
- registrar, cuando corresponda, información académica de su materia.

No puede, por defecto:

- consultar observaciones de otros docentes;
- consultar el desempeño global del alumno;
- consultar alertas globales;
- consultar información de otras materias;
- modificar registros realizados por otros docentes.

### 5.2. Preceptor / personal autorizado

El alcance exacto deberá definirse según la organización de la escuela.

Podrá tener acceso a información de seguimiento de los alumnos que estén bajo su responsabilidad institucional, con permisos superiores a los docentes pero inferiores o distintos a los del equipo directivo según corresponda.

### 5.3. Equipo directivo

Podrá:

- consultar la visión integral de los alumnos;
- visualizar tendencias y señales agregadas;
- consultar observaciones provenientes de diferentes materias;
- registrar intervenciones institucionales;
- responder solicitudes de información realizadas por docentes;
- realizar seguimiento de alumnos.

### 5.4. Administrador técnico

Se ocupará de:

- usuarios;
- roles;
- cursos;
- materias;
- horarios;
- configuraciones del sistema;
- mantenimiento técnico;
- auditoría y seguridad.

El acceso técnico a datos personales deberá ser limitado y auditado.

---

## 6. Gestión del ciclo de vida de alumnos, profesores, cursos y asignaciones

El sistema no debe asumir que la estructura escolar permanece fija durante el año. La realidad institucional incluye **altas, bajas, cambios de curso, promociones, suplencias y reemplazos docentes**. Estos eventos deben formar parte del modelo desde el comienzo.

### 6.1. Altas y bajas de alumnos

Un alumno puede ingresar a la institución durante el ciclo lectivo o retirarse antes de finalizarlo. El sistema debe permitir registrar fecha de ingreso, fecha de egreso/baja, motivo o tipo administrativo cuando corresponda y situación académica del alumno en ese momento.

El alumno no debe eliminarse físicamente de la base de datos por una baja, ya que sus registros históricos pueden seguir siendo necesarios para la institución. Debe pasar a un estado que indique que ya no se encuentra activo.

### 6.2. Ingresos durante el ciclo lectivo

Cuando ingresa un alumno nuevo, el sistema debe incorporarlo al curso y generar las relaciones necesarias con las materias y docentes vigentes desde su fecha de ingreso. Los datos anteriores a su ingreso institucional no deben confundirse con registros producidos dentro de la escuela.

### 6.3. Bajas y cambios de curso

Si un alumno cambia de división, orientación, turno u otra estructura institucional, el sistema debe conservar el historial anterior y registrar el nuevo contexto a partir de una fecha determinada.

La relación entre alumno y curso debe ser **histórica y fechada**, no simplemente un campo que se sobrescribe cada año.

### 6.4. Profesores, suplencias y reemplazos

Los profesores también tienen un ciclo de vida dentro del sistema. Deben contemplarse situaciones como:

- alta de un docente nuevo;
- baja o desvinculación;
- licencia;
- suplencia temporal;
- reemplazo definitivo;
- cambio de materia o curso;
- modificación del horario.

Una suplencia no debe borrar la relación histórica con el docente titular. Debe registrarse como una **asignación temporal**, con fecha de inicio y finalización.

Esto permite reconstruir correctamente quién estaba a cargo de una materia cuando se produjo una observación.

### 6.5. Cierre e inicio de cada año escolar

El sistema debe tener un proceso explícito de transición entre ciclos lectivos. Al finalizar el año se deberá poder cerrar el período y preparar el siguiente sin perder el historial.

En el nuevo año, la mayoría de los alumnos podrá pasar al curso siguiente, mientras que otros podrían:

- permanecer en el mismo grado;
- cambiar de orientación/división;
- egresar;
- trasladarse;
- ingresar desde otra institución.

El **paso de grado no debe editar el historial del año anterior**. Debe generar una nueva asignación para el ciclo lectivo siguiente.

Ejemplo:

```text
2026 → 3° B
        ↓ fin de ciclo
2027 → 4° B
```

El sistema debe poder mantener ambos contextos simultáneamente como parte del historial del alumno.

### 6.6. Configuración por ciclo lectivo

Se recomienda que cursos, divisiones, materias, horarios y asignaciones docentes estén vinculados explícitamente a un **ciclo lectivo**. Esto simplifica el cierre anual, la promoción de alumnos y la reconstrucción histórica.

---

## 7. Principio de separación de información

Una decisión central del proyecto es **no mostrar automáticamente al profesor el desempeño global de un alumno**.

Esto responde a una preocupación de diseño: conocer anticipadamente las observaciones de otros docentes puede influir sobre la percepción y las futuras observaciones de un profesor.

El sistema buscará preservar una cierta independencia entre las observaciones.

### Flujo propuesto

```text
Profesor observa al alumno
        ↓
Registra una observación en su contexto
        ↓
El sistema almacena el evento
        ↓
El profesor NO ve automáticamente la información de otras materias
        ↓
El sistema agrega los datos para usuarios autorizados
        ↓
Equipo directivo analiza la visión global
```

### Solicitud de información

Si un profesor considera necesario conocer el estado general de un alumno, podrá realizar una **solicitud de seguimiento o información** al equipo autorizado.

La solicitud deberá quedar registrada y el equipo directivo decidirá qué información corresponde proporcionar.

Este mecanismo permite conciliar dos objetivos:

- brindar información cuando sea pedagógicamente necesaria;
- reducir el riesgo de introducir sesgos previos en las observaciones docentes.

---

## 8. Registro contextual de las observaciones

Una observación no debe existir como un dato aislado.

El sistema debe conocer la relación institucional entre:

```text
Profesor
   ↓
Materia
   ↓
Curso / División
   ↓
Alumno
```

Además, deberá incorporar el horario de la asignatura.

### Ejemplo

Un profesor de Matemática tiene asignada la siguiente clase:

```text
Profesor: Juan García
Materia: Matemática
Curso: 3° B
Día: lunes
Horario: 08:00 - 09:00
```

Si registra una observación a las 08:37, el sistema puede establecer que el evento se produjo **dentro del horario de la clase correspondiente**.

Si se registra a las 18:42, el sistema deberá identificar que se produjo **fuera del horario habitual de esa asignatura**.

Esto no implica necesariamente impedir el registro; en ciertos casos puede ser legítimo realizar una carga administrativa posterior. Sin embargo, el contexto horario debe quedar guardado.

---

## 9. Categorías iniciales de observación

Las categorías definitivas deberán surgir de una revisión específica de literatura educativa y de los objetivos institucionales. No se propone abrir inicialmente un sistema ilimitado de categorías definido por votación de usuarios.

La primera versión puede utilizar un conjunto pequeño de categorías basadas en conductas observables.

### Participación

- Participación adecuada / activa
- Participación disminuida
- No participa

### Trabajo académico

- Realiza las actividades
- No completa la actividad
- No entrega el trabajo solicitado
- No dispone del material necesario

### Atención

- Mantiene la atención
- Presenta distracciones frecuentes

### Convivencia

- Interacción adecuada
- Conflicto con pares
- Conducta disruptiva

### Evolución

- Mejora observada
- Deterioro observado

### Otra situación

Permite registrar una situación no contemplada.

Cuando se utiliza esta opción, se recomienda solicitar un comentario explicativo.

---

## 10. Registro de eventos positivos

El sistema no debe utilizarse únicamente para acumular problemas. También debe permitir registrar hechos positivos que ayuden a comprender la evolución y las fortalezas del alumno.

Esto es importante por dos motivos. Primero, una base de datos compuesta solamente por eventos negativos puede producir una visión distorsionada del alumno. Segundo, la institución puede estar interesada en detectar tempranamente **fortalezas, talentos, intereses y desempeños sobresalientes** que justifiquen oportunidades adicionales.

Ejemplos de eventos positivos:

- mejora significativa;
- participación destacada;
- desempeño académico excepcional;
- liderazgo positivo;
- colaboración con compañeros;
- creatividad o resolución destacada de problemas;
- interés excepcional por una materia o área;
- constancia y autonomía;
- superación de una dificultad previamente observada.

El sistema no debería asumir que todo alumno necesita seguimiento. Es esperable que **la mayoría de los alumnos no genere alertas relevantes**. La ausencia de alertas debe poder distinguirse claramente de la ausencia de datos o de una falla del sistema.

Se propone distinguir tres estados generales:

- **Sin señales relevantes:** existe información suficiente y no se detectan patrones que requieran intervención especial.
- **Información insuficiente:** todavía no existe una cantidad o calidad de datos adecuada para realizar una interpretación responsable.
- **Señales para revisión:** existen cambios o combinaciones de eventos que justifican una revisión institucional.

La misma arquitectura utilizada para detectar señales de atención puede utilizarse, con reglas diferentes, para detectar oportunidades de estímulo: becas, proyectos, olimpíadas, tutorías, actividades extracurriculares u otras propuestas institucionales.

La detección de fortalezas deberá realizarse con criterios claros y revisión humana. Una única observación positiva no debería convertirse automáticamente en una etiqueta permanente, del mismo modo que una única observación negativa no debería convertirse en una etiqueta problemática.

## 11. Calificaciones

Las calificaciones serán una parte del sistema, pero no constituirán el centro del proyecto.

Podrán incorporarse como una de las familias de información utilizadas para interpretar tendencias.

Por ejemplo:

```text
Observaciones de participación
        +
Asistencia
        +
Rendimiento académico
        ↓
Análisis de evolución
```

No se propone inicialmente crear una "nota de comportamiento".

Una puntuación única para el comportamiento puede transmitir una precisión inexistente y favorecer interpretaciones simplistas.

Es preferible trabajar con eventos observables y posteriormente analizar su frecuencia, recencia y evolución.

---

## 12. Asistencia y horario

La asistencia puede ser incorporada como otra fuente de información importante.

La literatura sobre sistemas de alerta temprana identifica la asistencia, el comportamiento y el desempeño académico como familias centrales de indicadores.

En una primera etapa, el sistema deberá al menos ser capaz de almacenar y eventualmente relacionar:

- fecha;
- curso;
- alumno;
- asignatura;
- docente;
- asistencia o inasistencia;
- llegada tarde, cuando corresponda.

El diseño futuro deberá definir quién registra esta información y con qué reglas institucionales.

---

## 13. Motor de indicadores y alertas

Las alertas no deberán surgir de una única observación aislada.

El objetivo es identificar **patrones o cambios recientes**.

### Ejemplo conceptual

```text
Alumno A

Semana 1 → 1 observación de baja participación
Semana 2 → 2 observaciones
Semana 3 → 3 observaciones
Semana 4 → observaciones en 3 materias

                     ↓

        Señal de seguimiento
```

El sistema podrá analizar, entre otros aspectos:

- cantidad de eventos;
- frecuencia;
- recencia;
- tendencia;
- número de materias involucradas;
- combinación con asistencia;
- combinación con rendimiento académico;
- evolución positiva o negativa.

### Niveles provisionales

**Verde — seguimiento normal**

No se observan cambios relevantes según las reglas actuales.

**Amarillo — atención**

Aparecen algunas señales que conviene observar.

**Naranja — seguimiento**

Se acumulan señales o aparecen en varias materias.

**Rojo — revisión institucional**

La combinación de indicadores justifica una revisión por parte del equipo autorizado.

> Estos niveles son conceptos de diseño, no umbrales definitivos. Los valores concretos deberán estudiarse con datos reales de la institución y validarse pedagógicamente.

---

## 14. Las alertas no son diagnósticos

Esta distinción debe quedar explícita tanto en el diseño como en la interfaz.

El sistema no deberá presentar mensajes como:

> "Alumno problemático"

> "Alumno de alto riesgo"

> "Alumno con problemas"

Preferentemente utilizará expresiones como:

> "Se detectaron señales recientes que requieren revisión."

> "Se observa un cambio reciente en determinados indicadores."

> "Se recomienda revisar la evolución del alumno."

La decisión final debe corresponder al personal educativo autorizado.

---

## 15. Panel del profesor

La experiencia de uso del profesor debe estar optimizada para velocidad.

### Pantalla principal conceptual

```text
┌───────────────────────────────┐
│       2° B — MATEMÁTICA       │
├───────────────────────────────┤
│                               │
│ Juan Pérez                    │
│                               │
│ ¿Qué observaste?              │
│                               │
│ [ Participación adecuada ]    │
│ [ Baja participación ]        │
│ [ No completó actividad ]     │
│ [ No entregó trabajo ]        │
│ [ Dificultad persistente ]    │
│ [ Conducta disruptiva ]       │
│ [ Conflicto ]                 │
│ [ Mejora ]                    │
│                               │
│ [+ Agregar comentario]        │
│                               │
│          [ REGISTRAR ]        │
└───────────────────────────────┘
```

Objetivo: **registrar la mayoría de las observaciones con uno o pocos toques**.

---

## 16. Panel del equipo directivo

El equipo directivo necesita una interfaz diferente.

El profesor necesita rapidez; el directivo necesita síntesis y contexto.

### Panel conceptual

```text
┌──────────────────────────────────────┐
│       PANEL DE SEGUIMIENTO           │
├──────────────────────────────────────┤
│                                      │
│ 🟢 Seguimiento normal       180      │
│ 🟡 Atención                   24      │
│ 🟠 Seguimiento                 9      │
│ 🔴 Revisión institucional      3      │
│                                      │
├──────────────────────────────────────┤
│ CAMBIOS RECIENTES                    │
│                                      │
│ Juan Pérez       3° B       ↑       │
│ María López      2° A       ↓       │
│ Pedro García     4° B       ↓       │
│                                      │
└──────────────────────────────────────┘
```

Desde allí se podrá acceder a una ficha integral del alumno.

---

## 17. Ficha integral del alumno

Esta información estará reservada para los roles autorizados.

La ficha puede mostrar:

- datos básicos del alumno;
- curso/división;
- evolución temporal;
- asistencia;
- rendimiento académico;
- observaciones estructuradas;
- distribución por materias;
- señales recientes;
- intervenciones institucionales;
- evolución posterior a una intervención.

Ejemplo conceptual:

```text
JUAN PÉREZ — 3° B

Últimos 30 días

Participación       ↑ señales
Trabajo académico   ↑ señales
Asistencia          → normal
Rendimiento         ↓ tendencia

Materias involucradas:
Matemática          🟠
Lengua              🟡
Historia            🟠
Biología            🟢

[ Ver evolución ]
[ Ver observaciones ]
[ Registrar seguimiento ]
```

---

## 18. Solicitud de información entre profesores y dirección

Si un docente considera necesario conocer la evolución general de un alumno, podrá generar una solicitud.

Ejemplo:

```text
Juan Pérez — 3° B

[ Solicitar información de seguimiento ]

Motivo:
________________________________

[ ENVIAR SOLICITUD ]
```

El equipo directivo podrá:

- aprobar;
- rechazar;
- responder parcialmente;
- solicitar más información;
- registrar una intervención.

La solicitud y la respuesta deberán quedar auditadas.

---

## 19. Modelo conceptual inicial de datos

Una primera versión puede incluir las siguientes entidades.

### Alumno

- id
- nombre
- apellido
- DNI u otro identificador institucional, según la normativa y necesidad
- curso/división
- estado de matrícula

### Profesor

- id
- nombre
- apellido
- usuario
- rol
- estado

### Materia

- id
- nombre

### Curso / División

- id
- año
- división
- turno

### Asignación docente

Relaciona:

```text
Profesor + Materia + Curso + Horario
```

### Observación

- id
- alumno
- profesor
- materia
- curso
- categoría
- fecha
- hora
- comentario opcional
- contexto horario
- estado
- fecha de creación

### Registro académico

Puede incluir calificaciones u otros datos académicos según el alcance que se defina.

### Asistencia

- alumno
- fecha
- materia / módulo, si corresponde
- estado
- docente o usuario responsable

### Solicitud de seguimiento

- alumno
- profesor solicitante
- fecha
- motivo
- estado
- respuesta
- usuario que respondió

### Intervención institucional

- alumno
- fecha
- responsable
- tipo de intervención
- observación
- seguimiento posterior

### Asignación alumno-curso por ciclo lectivo

Debe registrar el contexto histórico del alumno:

- alumno;
- ciclo lectivo;
- curso/división;
- fecha de inicio;
- fecha de finalización;
- condición o tipo de asignación.

### Asignación docente-materia-curso

Permite representar titulares y suplentes:

- docente;
- materia;
- curso/división;
- fecha de inicio;
- fecha de finalización;
- tipo de asignación (titular, suplente, reemplazo u otro).

### Ciclo lectivo

- año;
- fecha de inicio;
- fecha de finalización;
- estado (planificado, activo, cerrado).

### Catálogo de observaciones

- id;
- nombre;
- categoría;
- definición;
- criterio de uso;
- estado (activo/inactivo);
- versión;
- usuario que creó/modificó;
- fecha de vigencia.

### Auditoría

Registro de acciones relevantes del sistema.

---

## 20. Seguridad y privacidad

Este componente debe formar parte de la arquitectura desde el inicio.

El sistema manejará información sobre menores de edad y datos académicos y conductuales.

Por ello deberán contemplarse, como mínimo:

- autenticación de usuarios;
- contraseñas seguras y recuperación controlada;
- control de acceso basado en roles;
- principio de mínimo privilegio;
- separación de información por materia y función;
- cifrado de las comunicaciones;
- copias de seguridad;
- registros de auditoría;
- protección contra accesos indebidos;
- políticas de conservación y eliminación de datos;
- mecanismos para corregir información errónea;
- procedimientos ante incidentes de seguridad.

También deberá determinarse qué información puede ser visible para cada función institucional.

La normativa específica de protección de datos aplicable en Argentina y en la jurisdicción educativa deberá revisarse antes de utilizar datos reales.

---

## 21. Reglas de calidad de los datos

El valor futuro del sistema dependerá de la calidad de sus registros.

Por lo tanto, la aplicación deberá favorecer:

### Estandarización

Las observaciones frecuentes se registrarán mediante categorías comunes.

### Contexto

Cada evento deberá quedar relacionado con materia, curso, docente, fecha y hora.

### Consistencia

Las categorías deben tener definiciones claras.

### Separación entre hecho y opinión

El sistema debe orientar al profesor hacia conductas observables.

### Registro de positivos y negativos

Debe evitarse construir una base de datos donde solamente aparezcan problemas.

### Temporalidad

La fecha y hora son parte esencial de la información.

---

## 22. Consideraciones sobre sesgos

El diseño debe contemplar que los registros docentes pueden contener subjetividad.

La aplicación no elimina el sesgo por sí sola.

Por eso se proponen varias medidas:

1. Utilizar categorías de comportamiento observables.
2. No mostrar automáticamente al docente el historial global del alumno.
3. Registrar el contexto de cada evento.
4. No convertir eventos aislados en etiquetas permanentes.
5. Analizar tendencias y no únicamente conteos absolutos.
6. Permitir revisión humana por parte del equipo autorizado.
7. Auditar el funcionamiento de las reglas de alerta.
8. Revisar si ciertas categorías se utilizan de manera desproporcionada entre cursos, materias o grupos.

La etapa posterior de análisis de datos deberá estudiar también la posibilidad de **sesgos sistemáticos en los propios registros**.

---

## 23. Filosofía del sistema

El sistema no debe decidir por la escuela ni convertir señales en diagnósticos automáticos.

Su función es:

```text
OBSERVAR
   ↓
REGISTRAR
   ↓
ORGANIZAR
   ↓
DETECTAR CAMBIOS
   ↓
FACILITAR LA REVISIÓN
   ↓
APOYAR LA INTERVENCIÓN
```

La intervención continúa siendo una decisión humana e institucional.

---

## 24. Población sin alertas y detección de fortalezas

El sistema debe asumir desde su diseño que **la mayoría de los alumnos probablemente no requerirá una intervención especial en un momento determinado**. Esto es un resultado normal y deseable, no un defecto del sistema.

Por lo tanto, la aplicación no debe estar construida alrededor de la idea de que cada alumno necesita una alerta. El objetivo es identificar cambios relevantes sin producir una cantidad artificialmente elevada de reportes.

La lógica institucional debe poder reconocer dos grandes direcciones de seguimiento:

```text
                 DATOS DEL ALUMNO
                        │
            ┌───────────┴───────────┐
            ↓                       ↓
     SEÑALES DE ATENCIÓN      SEÑALES POSITIVAS
            ↓                       ↓
       Seguimiento            Oportunidades
            ↓                       ↓
      Intervención           Becas / proyectos /
                             estímulos / tutorías
```

Esto permite que el sistema cumpla dos funciones complementarias:

- **prevención y acompañamiento**, cuando aparecen señales de deterioro, dificultades o cambios preocupantes;
- **detección de oportunidades**, cuando aparecen fortalezas, talentos, intereses o mejoras que podrían justificar una propuesta educativa adicional.

La ausencia de alertas negativas no significa que el sistema no esté funcionando. Una institución saludable debería tener numerosos alumnos sin señales de seguimiento y, al mismo tiempo, algunos alumnos con necesidades de apoyo y otros con oportunidades de desarrollo especial.

Además, el sistema debe evitar confundir **ausencia de reportes** con **ausencia de problemas**. La interpretación de un alumno debe tener en cuenta la cantidad y calidad de información disponible, la duración de su permanencia en la institución y las materias o períodos efectivamente observados.

---

## 25. Primera versión funcional propuesta — MVP

La primera versión no debería intentar abarcar todo el sistema escolar.

### Funciones para profesores

- inicio de sesión;
- selección de curso;
- lista de alumnos;
- registro rápido de observación;
- comentario opcional;
- registro automático de fecha y hora;
- validación de materia/curso/horario;
- consulta de sus propios registros.

### Funciones para directivos

- inicio de sesión;
- búsqueda de alumnos;
- vista integral;
- filtros por curso y materia;
- evolución temporal;
- observaciones agregadas;
- identificación de cambios recientes;
- identificación de fortalezas y eventos positivos;
- registro de seguimiento;
- gestión de solicitudes de información de docentes;
- administración del catálogo de observaciones;
- gestión de altas y bajas de alumnos y docentes, según permisos;
- gestión de cursos, materias, horarios y asignaciones.

### Fuera del MVP inicial

- inteligencia artificial;
- modelos predictivos complejos;
- puntuaciones automáticas de "riesgo" con pretensión diagnóstica;
- integración con múltiples sistemas externos;
- aplicación móvil nativa independiente;
- funciones administrativas no relacionadas con el objetivo principal.

---

## 26. Estrategia tecnológica preliminar

### Primera elección recomendada

Desarrollar una **aplicación web responsive**, accesible desde celulares y computadoras.

Esto permite que los docentes utilicen el sistema desde el teléfono sin obligarlos a instalar y actualizar una aplicación nativa.

### Arquitectura preliminar

```text
                 NAVEGADOR / CELULAR
                         │
                         ↓
                    Aplicación web
                         │
                         ↓
                       API
                         │
                         ↓
                 Base de datos
                         │
                         ↓
                Motor de indicadores
```

### Tecnologías posibles

**Frontend**

- HTML/CSS/JavaScript para una primera implementación sencilla;
- React u otra tecnología similar cuando sea necesario escalar la interfaz.

**Backend**

- Python;
- Django o FastAPI.

**Base de datos**

- PostgreSQL.

**Análisis de datos**

- Python;
- pandas;
- herramientas estadísticas;
- posteriormente, si la calidad y cantidad de datos lo justifican, modelos de machine learning.

La elección tecnológica definitiva deberá realizarse después de definir el modelo de datos, los permisos y los requisitos de infraestructura.

---

## 27. Evolución futura del proyecto

Una posible evolución sería:

```text
FASE 1
Registro estructurado
        ↓
FASE 2
Panel institucional
        ↓
FASE 3
Indicadores y reglas simples
        ↓
FASE 4
Análisis estadístico
        ↓
FASE 5
Evaluación de modelos predictivos
        ↓
FASE 6
Mejora continua del sistema
```

La inteligencia artificial o el machine learning **no deben ser el punto de partida**.

Primero se necesita una base de datos consistente, una definición clara de las variables y un proceso institucional sólido.

---

## 28. Preguntas que deben resolverse antes de programar

1. ¿Cuál es exactamente el alcance institucional de cada rol?
2. ¿Quién administra alumnos, profesores, cursos, materias y horarios?
3. ¿Quién puede registrar cada tipo de información?
4. ¿Quién puede modificar o corregir un registro?
5. ¿Qué información se considera estrictamente confidencial?
6. ¿Cuánto tiempo debe conservarse cada tipo de registro?
7. ¿Cómo se corrige una observación errónea?
8. ¿Qué categorías de observación resultan suficientemente objetivas?
9. ¿Cuáles son los eventos que realmente interesa detectar tempranamente?
10. ¿Qué combinaciones de señales deberían generar una revisión?
11. ¿Quién recibe y resuelve las alertas?
12. ¿Qué acciones quedan registradas después de una alerta?
13. ¿Cómo se evalúa si el sistema realmente ayuda a intervenir antes?
14. ¿Qué normativa y políticas de protección de datos deben cumplirse?
15. ¿Dónde se alojará la información y quién tendrá administración técnica?
16. ¿Qué datos o comportamientos adicionales puede incorporar el administrador/directivo al catálogo institucional?
17. ¿Qué criterios diferenciarán una señal de atención, una señal positiva y un simple registro informativo?
18. ¿Cómo se gestionará un alumno que ingresa o se retira durante el ciclo lectivo?
19. ¿Cómo se gestionarán promociones, repitencias, cambios de división y egresos entre años?
20. ¿Cómo se representarán suplencias y reemplazos docentes sin perder el historial?
21. ¿Qué ocurre con las observaciones y permisos de un docente cuando finaliza su asignación?
22. ¿Cómo se distinguirán los alumnos sin señales relevantes de aquellos sobre los que todavía no existen suficientes datos?
23. ¿Qué oportunidades institucionales pueden asociarse a señales positivas de talento, interés o mejora?

---

## 29. Próxima etapa recomendada

Antes de comenzar a programar la interfaz, se recomienda producir un **modelo conceptual y funcional detallado**.

Ese documento deberá definir:

1. entidades y relaciones;
2. roles y permisos;
3. ciclo lectivo y estados históricos;
4. altas, bajas y promociones de alumnos;
5. altas, bajas y asignaciones temporales de docentes;
6. flujo de una observación;
7. catálogo inicial y mecanismo controlado para agregar nuevas categorías;
8. reglas de validación y contexto horario;
9. separación entre observaciones negativas, positivas e informativas;
10. solicitudes de información;
11. intervención institucional;
12. auditoría;
13. requisitos de seguridad;
14. primer modelo de base de datos;
15. pantallas mínimas del MVP.

El resultado será una especificación suficientemente precisa para comenzar después el desarrollo técnico.

---

## 30. Referencias iniciales

- Institute of Education Sciences (IES). Recursos sobre **Early Warning Systems** y uso de indicadores educativos.
- Regional Educational Laboratory (REL). Materiales sobre diseño y utilización de sistemas de alerta temprana.
- U.S. Department of Education — Student Privacy. Principios de acceso autorizado y protección de datos educativos.

### Recursos consultados durante la etapa inicial

- IES / REL West — recursos sobre sistemas e indicadores de alerta temprana: https://ies.ed.gov/rel-west/2025/01/guide
- IES / REL Northwest — estudios sobre implementación de sistemas de alerta temprana: https://ies.ed.gov/rel-northwest/2025/01/descriptive-study-2
- IES — estudio de impacto sobre sistemas de intervención y alerta temprana: https://ies.ed.gov/use-work/resource-library/report/impact-study/getting-students-track-graduation-impacts-early-warning-intervention-and-monitoring-system-after-one
- IES — guía sobre creación de indicadores para sistemas de alerta temprana: https://ies.ed.gov/use-work/resource-library/resource/other-resource/district-guide-creating-indicators-early-warning-systems
- U.S. Department of Education — Student Privacy: https://studentprivacy.ed.gov/

> **Advertencia:** Las referencias anteriores son una base de investigación inicial y no constituyen por sí solas asesoramiento jurídico. Antes de una implementación real deberán revisarse las normas argentinas, provinciales/municipales y las políticas institucionales aplicables.

---

## 31. Idea rectora del proyecto

> **El sistema no busca etiquetar alumnos. Busca ayudar a la escuela a detectar cambios a tiempo.**

El valor del proyecto estará en conseguir que una observación que hoy se pierde entre conversaciones pueda transformarse en información institucional útil, sin convertir al docente en un operador administrativo, sin eliminar la interpretación humana y sin crear un historial que predisponga innecesariamente a quienes trabajan con el alumno.

