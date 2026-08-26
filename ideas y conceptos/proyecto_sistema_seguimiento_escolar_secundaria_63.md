# Sistema Institucional de Seguimiento Integral del Alumno
## Escuela Secundaria N.º 63

**Documento de alcance y lineamientos tecnológicos — Versión 0.3**

---

## 1. Propósito del documento

Este documento establece una primera definición del alcance institucional, funcional y tecnológico de un sistema destinado a la **Escuela Secundaria N.º 63**, contemplando desde el comienzo la posibilidad de que, si la experiencia resulta exitosa, el sistema sea utilizado por la totalidad de la escuela.

La solución no se plantea como una prueba aislada o descartable, sino como una **primera versión operativa de una plataforma institucional escalable**, capaz de comenzar con un conjunto reducido de usuarios y crecer progresivamente sin necesidad de rediseñar su arquitectura fundamental.

La escuela cuenta con **dos turnos: mañana y tarde**. El sistema deberá considerar esta estructura desde el diseño inicial.

---

## 2. Problema que se busca resolver

Un alumno interactúa con múltiples docentes, materias y espacios institucionales. Cada profesor observa solamente una parte de su trayectoria cotidiana, por lo que pueden existir señales relevantes que permanecen aisladas dentro de una sola materia.

Actualmente, para obtener una visión transversal del alumno suele ser necesario que los docentes se comuniquen entre sí de manera informal o que el equipo directivo reconstruya la situación a partir de conversaciones, reuniones y registros dispersos.

Esto presenta varias dificultades:

- la información puede no llegar a tiempo;
- algunos hechos relevantes pueden no quedar registrados;
- los docentes tienen información parcial;
- la comunicación entre muchos docentes es difícil de sostener sistemáticamente;
- la intervención institucional puede producirse recién cuando el problema ya se refleja en las calificaciones o en otras consecuencias visibles.

El sistema busca generar un **registro estructurado, contextualizado y longitudinal** de señales académicas, conductuales y de evolución del alumno para facilitar una intervención institucional temprana.

---

## 3. Principio central del sistema

El **alumno es la entidad principal del sistema**.

Los docentes no construyen una evaluación global del alumno. Cada docente aporta observaciones vinculadas exclusivamente con el contexto en el que tiene responsabilidad: su materia, curso, turno y horario.

El sistema permite que la información de múltiples fuentes sea organizada y analizada institucionalmente, pero la **visión integral queda reservada a los roles autorizados**.

La lógica general es:

```text
DOCENTE
   ↓
OBSERVA
   ↓
REGISTRA UN EVENTO
   ↓
SISTEMA CONTEXTUALIZA Y ALMACENA
   ↓
SE ACUMULAN DATOS DE DISTINTAS MATERIAS
   ↓
SISTEMA GENERA INDICADORES
   ↓
EQUIPO AUTORIZADO REVISA
   ↓
INTERVENCIÓN / ACOMPAÑAMIENTO
   ↓
SEGUIMIENTO DE LA EVOLUCIÓN
```

---

## 4. Alcance institucional

### 4.1 Alcance inicial

El sistema será diseñado específicamente para la **Escuela Secundaria N.º 63** y contemplará:

- turno mañana;
- turno tarde;
- cursos y divisiones de ambos turnos;
- profesores titulares, suplentes y otras asignaciones temporales autorizadas;
- alumnos regulares;
- altas y bajas durante el ciclo lectivo;
- movimientos de alumnos entre cursos o divisiones;
- cambios de docentes y suplencias;
- cierre y apertura de ciclos lectivos;
- historial escolar dentro del sistema.

### 4.2 Alcance de crecimiento

Aunque inicialmente el sistema será utilizado únicamente por la Escuela Secundaria N.º 63, deberá soportar sin cambios estructurales importantes el crecimiento desde un conjunto reducido de usuarios hasta la participación de:

- todo el cuerpo docente;
- preceptoría y/o roles equivalentes;
- equipo directivo;
- personal administrativo autorizado;
- administrador técnico del sistema.

El crecimiento previsto es **institucional dentro de la escuela**, no una plataforma multiescuela en su primera etapa.

---

## 5. Objetivos

### 5.1 Objetivo principal

Construir un sistema institucional que permita registrar y organizar señales relevantes sobre la trayectoria de los alumnos para facilitar la **detección temprana de necesidades de acompañamiento**, así como la identificación de fortalezas y oportunidades de desarrollo.

### 5.2 Objetivos específicos

1. Facilitar a los docentes un mecanismo de registro extremadamente rápido.
2. Mantener los registros contextualizados por materia, curso, turno, docente y horario.
3. Restringir el acceso según el rol y la responsabilidad institucional de cada usuario.
4. Evitar que un docente necesite conocer la información global de un alumno para registrar sus propias observaciones.
5. Permitir al equipo autorizado consultar una visión transversal del alumno.
6. Detectar patrones y cambios a lo largo del tiempo.
7. Identificar tempranamente señales que requieran seguimiento.
8. Detectar también comportamientos positivos, fortalezas y alumnos con desempeño sobresaliente.
9. Mantener un historial institucional que sobreviva a cambios de curso, docentes y ciclos lectivos.
10. Proporcionar una base de datos apta para análisis estadístico futuro.

---

## 6. Filosofía de registro: hechos antes que diagnósticos

La aplicación deberá favorecer el registro de **conductas o hechos observables** en lugar de juicios globales sobre el alumno.

Se debe preferir:

> "No realizó la actividad propuesta."

frente a:

> "Es irresponsable."

Se debe preferir:

> "Se quedó dormido durante la clase."

frente a:

> "No le interesa estudiar."

Esta distinción permite mejorar la calidad del dato, reducir interpretaciones subjetivas y facilitar análisis posteriores.

El sistema no deberá presentar los registros como diagnósticos psicológicos, médicos ni sociales.

---

## 7. Registro rápido del docente

La interfaz docente deberá estar diseñada para que el registro cotidiano pueda realizarse en pocos segundos.

El flujo esperado es:

```text
Seleccionar alumno
        ↓
Seleccionar comportamiento / evento
        ↓
Guardar
```

El comentario libre será opcional en la mayoría de los casos y obligatorio solamente cuando la naturaleza del evento requiera contexto adicional.

### 7.1 Ejemplos de categorías iniciales

Las categorías deberán establecerse a partir de revisión académica y de criterios institucionales, no mediante una lista abierta de sugerencias docentes.

Podrán incluir, entre otras:

**Participación**

- participación adecuada;
- participación disminuida;
- ausencia de participación.

**Trabajo académico**

- realiza las actividades;
- no completa la actividad;
- no entrega trabajos;
- no dispone de los materiales necesarios.

**Atención**

- atención adecuada;
- distracciones frecuentes;
- se queda dormido durante la clase.

**Comportamiento / convivencia**

- comportamiento adecuado;
- conducta disruptiva;
- conflicto con pares;
- dificultad para respetar pautas de convivencia.

**Estado observable / evolución**

- apatía observable;
- aislamiento observable;
- tristeza observable;
- cambio positivo observable;
- mejora significativa;
- actitud especialmente participativa;
- desempeño sobresaliente.

La inclusión de categorías relacionadas con estado emocional deberá definirse con especial cuidado para que representen **observaciones visibles** y no diagnósticos o interpretaciones clínicas.

---

## 8. Registro de eventos positivos

El sistema no será exclusivamente un mecanismo para registrar problemas.

Se deberá permitir identificar señales positivas, por ejemplo:

- mejora sostenida;
- participación destacada;
- desempeño sobresaliente;
- colaboración con compañeros;
- liderazgo positivo;
- iniciativa;
- compromiso excepcional;
- evolución académica destacable.

La razón es doble:

1. evitar construir una imagen institucional del alumno basada únicamente en dificultades;
2. detectar tempranamente oportunidades de desarrollo.

Un alumno puede destacarse antes de obtener una calificación final sobresaliente y esa información puede resultar útil para oportunidades tales como:

- becas;
- proyectos institucionales;
- olimpíadas;
- actividades académicas especiales;
- programas de acompañamiento al talento;
- representación de la escuela en actividades externas.

El sistema deberá distinguir **necesidades de apoyo** de **oportunidades de desarrollo**.

---

## 9. Visibilidad de la información y prevención de sesgos

El docente no deberá disponer de una visión global automática del historial de un alumno.

### 9.1 El docente podrá

- consultar sus cursos y alumnos asignados;
- registrar observaciones correspondientes a su materia y responsabilidad;
- consultar sus propios registros;
- registrar evaluaciones o información académica que corresponda a su función;
- solicitar, cuando exista una razón institucional válida, información adicional sobre un alumno.

### 9.2 El docente no podrá

- consultar las observaciones registradas por otros docentes;
- consultar automáticamente indicadores de riesgo o seguimiento;
- consultar la visión global del alumno;
- consultar información institucional restringida;
- modificar registros de otros docentes salvo mediante un mecanismo autorizado.

### 9.3 Equipo directivo y roles autorizados

Podrán acceder a la visión transversal según sus permisos y responsabilidades.

Cuando un docente necesite conocer información global de un alumno, podrá existir un flujo de **solicitud de información a un rol autorizado**.

La solicitud y la respuesta deberán quedar auditadas.

---

## 10. Contextualización temporal y académica

Cada registro deberá incluir automáticamente el contexto institucional correspondiente.

Como mínimo:

- alumno;
- docente;
- materia;
- curso;
- división;
- turno;
- fecha;
- hora;
- ciclo lectivo;
- tipo de evento;
- comentario, cuando corresponda.

### 10.1 Validación del horario

El sistema deberá conocer las asignaciones y horarios correspondientes a docentes, materias, cursos y turnos.

Al registrar un evento, podrá determinar si el docente se encontraba dentro del horario previsto para esa clase.

Esto permitirá distinguir, por ejemplo:

```text
Registro durante la clase
Registro fuera del horario de clase
```

El registro fuera de horario no necesariamente deberá bloquearse, pero la condición deberá quedar registrada y podrá requerir un nivel adicional de justificación según las reglas institucionales.

---

## 11. Roles y control de acceso

La seguridad se basará en **roles y permisos**, no solamente en autenticación.

### 11.1 Roles iniciales

#### Docente

Acceso limitado a los cursos y materias que tenga asignados.

#### Preceptor / rol equivalente

Acceso a los alumnos y funciones correspondientes a su ámbito institucional.

#### Equipo directivo

Acceso transversal a la información que corresponda a su función.

#### Administrador institucional

Gestiona usuarios, asignaciones, catálogos, parámetros y configuración operativa.

#### Administrador técnico

Gestiona la infraestructura y aspectos técnicos del sistema sin asumir necesariamente funciones pedagógicas.

La separación entre administrador institucional y administrador técnico deberá evaluarse durante el diseño definitivo.

---

## 12. Gestión del ciclo de vida de alumnos

El sistema deberá soportar cambios administrativos normales sin perder el historial.

### 12.1 Alta de alumno

Debe ser posible incorporar alumnos al sistema durante el ciclo lectivo.

El alta deberá incluir:

- datos básicos;
- ciclo lectivo;
- curso/división;
- turno;
- fecha de ingreso;
- situación institucional correspondiente.

### 12.2 Baja de alumno

Debe ser posible registrar egresos, traslados, pases u otras bajas institucionales.

La baja no deberá eliminar automáticamente el historial.

### 12.3 Cambio de curso o división

El alumno podrá pasar de una división a otra conservando su historial anterior.

Debe registrarse:

- curso anterior;
- curso nuevo;
- fecha del cambio;
- motivo o categoría administrativa cuando corresponda.

### 12.4 Cierre del ciclo lectivo

Al finalizar el año, el sistema deberá permitir registrar la situación del alumno:

- promoción;
- repitencia;
- egreso;
- traslado;
- otra situación institucional definida.

### 12.5 Comienzo de un nuevo ciclo

Los alumnos que continúan deberán recibir una **nueva asignación al curso del nuevo ciclo lectivo**, sin alterar el historial del ciclo anterior.

Conceptualmente:

```text
Alumno
  │
  ├── Ciclo 2026 → 3° B
  │
  └── Ciclo 2027 → 4° B
```

La historia permanece vinculada al alumno y cada asignación pertenece a un ciclo lectivo determinado.

---

## 13. Gestión del ciclo de vida de docentes

El sistema también deberá soportar cambios en el cuerpo docente.

Debe contemplar:

- altas de docentes;
- bajas;
- licencias;
- suplencias;
- cambios temporales de asignación;
- reasignaciones;
- finalización de una suplencia.

La relación entre docente, materia y curso deberá modelarse como una **asignación temporal y no como un atributo permanente del docente**.

Ejemplo:

```text
Docente A
Matemática — 3° B
01/03/2026 → 20/06/2026

Docente B
Matemática — 3° B
21/06/2026 → 30/09/2026

Docente A
Matemática — 3° B
01/10/2026 → fin del ciclo
```

Los registros históricos deberán conservar quién registró cada evento, independientemente de quién ocupe posteriormente la función.

---

## 14. Estructura institucional de dos turnos

Desde el diseño inicial, el sistema debe considerar que la Escuela Secundaria N.º 63 posee:

- **Turno mañana**
- **Turno tarde**

El turno deberá ser una dimensión formal del modelo de datos y no un texto introducido libremente por los usuarios.

Esto permitirá:

- filtrar información por turno;
- administrar horarios diferentes;
- asignar docentes y cursos correctamente;
- evitar conflictos de asignación;
- analizar indicadores por turno si fuese necesario;
- soportar una futura expansión sin rediseñar el modelo.

---

## 15. Indicadores y alertas

La primera versión del sistema no deberá diagnosticar ni etiquetar a los alumnos.

Debe detectar **señales que justifican revisión**.

Ejemplos:

```text
🟢 Sin señales relevantes

🟡 Señales recientes

🟠 Seguimiento recomendado

🔴 Revisión institucional prioritaria
```

Estos estados serán indicadores operativos y no diagnósticos.

### 15.1 Fuentes posibles de señales

- comportamiento;
- participación;
- trabajo académico;
- asistencia, cuando esté integrada;
- rendimiento académico;
- evolución positiva;
- observaciones de distintas materias;
- tendencias temporales.

### 15.2 Ausencia de reportes

La ausencia de observaciones negativas **no debe interpretarse automáticamente como ausencia de problemas**.

Puede significar:

- situación normal;
- falta de necesidad de intervención;
- falta de observación;
- baja frecuencia de uso del sistema;
- datos insuficientes.

El sistema deberá diferenciar, cuando sea posible, entre **sin señales relevantes** y **sin información suficiente**.

---

## 16. Indicadores positivos y detección de oportunidades

Deberá existir una línea paralela a la detección de dificultades:

```text
NECESIDAD DE APOYO
        ↕
TRAYECTORIA NORMAL
        ↕
FORTALEZA / OPORTUNIDAD
```

El sistema podrá ayudar a detectar tempranamente alumnos que presenten:

- desempeño sobresaliente;
- progreso excepcional;
- interés sostenido en determinada área;
- participación destacada;
- liderazgo positivo;
- capacidades que merezcan oportunidades especiales.

Las señales positivas podrán alimentar procesos institucionales para identificar candidatos a proyectos, becas y otras oportunidades, siempre mediante revisión humana.

---

## 17. Administración de categorías de observación

El sistema deberá permitir que un usuario institucional autorizado pueda **agregar o modificar categorías de observación** cuando exista una necesidad válida.

No se propone que cada docente personalice libremente sus categorías.

### 17.1 Requisitos del catálogo

Cada categoría debería tener:

- nombre;
- descripción;
- tipo o familia;
- carácter positivo, neutro o de atención;
- estado activo/inactivo;
- fecha de vigencia;
- versión;
- rol autorizado para administrarla.

Cuando una categoría deje de utilizarse, preferentemente deberá **desactivarse y no borrarse**, para conservar la interpretación de los registros históricos.

---

## 18. Auditoría y trazabilidad

Los datos institucionales deben permitir reconstruir qué ocurrió.

Cada registro relevante deberá conservar, como mínimo:

- quién lo creó;
- cuándo lo creó;
- a qué alumno corresponde;
- desde qué asignación docente se creó;
- si posteriormente fue modificado;
- quién realizó una modificación;
- cuándo ocurrió la modificación.

Las acciones sensibles, como solicitudes de información global, cambios de asignaciones, bajas, modificaciones administrativas y administración de categorías, deberán quedar auditadas.

---

## 19. Tecnología seleccionada

La tecnología elegida para el proyecto es:

### Backend

**Python + Django**

Django será responsable de:

- lógica de negocio;
- autenticación;
- autorización;
- administración;
- validaciones;
- gestión de sesiones;
- acceso a la base de datos;
- exposición de servicios cuando sea necesario.

### Base de datos

**PostgreSQL**

Se utilizará como base de datos relacional principal por la naturaleza estructurada de la información y por la necesidad de mantener relaciones, restricciones, integridad y consultas complejas.

### Interfaz

**Aplicación web responsive**, accesible desde:

- celulares Android;
- iPhone;
- tablets;
- computadoras.

La primera versión podrá utilizar Django Templates, HTML, CSS y JavaScript sin introducir innecesariamente una arquitectura frontend separada.

React u otra tecnología frontend podrá evaluarse posteriormente si la complejidad de la interfaz lo justifica.

### Análisis de datos

El análisis futuro podrá desarrollarse mediante Python y herramientas del ecosistema de ciencia de datos, por ejemplo:

- pandas;
- NumPy;
- herramientas estadísticas;
- visualización de datos;
- modelos de aprendizaje automático, únicamente en etapas posteriores y bajo criterios metodológicos y éticos adecuados.

---

## 20. Arquitectura general propuesta

```text
                  USUARIOS
                     │
         ┌───────────┴───────────┐
         │                       │
      CELULAR                 PC/TABLET
         │                       │
         └───────────┬───────────┘
                     ↓
               NAVEGADOR WEB
                     ↓
              ┌─────────────┐
              │   DJANGO    │
              │  Backend    │
              └──────┬──────┘
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
   AUTENTICACIÓN /          LÓGICA DE
     PERMISOS                NEGOCIO
          │                     │
          └──────────┬──────────┘
                     ↓
                POSTGRESQL
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
    Alumnos      Asignaciones   Eventos
       │             │             │
       └─────────────┼─────────────┘
                     ↓
                INDICADORES
                     ↓
              EQUIPO AUTORIZADO
```

---

## 21. Escalabilidad esperada

Aunque el sistema se diseña solamente para la Escuela Secundaria N.º 63, se deberá adoptar desde el principio una arquitectura que soporte:

- incorporación gradual de todos los profesores;
- utilización simultánea en ambos turnos;
- crecimiento del número de registros durante varios años;
- consultas históricas;
- múltiples usuarios concurrentes;
- ampliación de funcionalidades sin reconstruir la base del sistema.

La escalabilidad buscada para la primera etapa es **institucional y funcional**, no una plataforma destinada a múltiples escuelas.

### 21.1 Principios técnicos

- base de datos relacional bien normalizada;
- índices donde las consultas los requieran;
- separación clara entre presentación, lógica y persistencia;
- permisos evaluados en servidor;
- validación de reglas de negocio en backend;
- uso de HTTPS;
- copias de seguridad automatizadas;
- registro y monitoreo de errores;
- posibilidad de crecimiento horizontal o vertical de infraestructura si el uso lo exige.

---

## 22. El sistema no será una aplicación exclusivamente móvil

La decisión de utilizar una **aplicación web responsive** es deliberada.

Se busca que un profesor pueda utilizar el sistema desde su teléfono sin necesidad de instalar o actualizar una aplicación nativa.

Ventajas:

- una única versión del sistema;
- actualizaciones centralizadas;
- compatibilidad con Android y iOS;
- acceso desde PC para directivos y administración;
- menor costo de mantenimiento;
- posibilidad de incorporar posteriormente una aplicación móvil nativa si fuese necesario.

---

## 23. El MVP funcional

Aunque el proyecto tendrá una arquitectura preparada para una adopción amplia, la primera entrega funcional se concentrará en el núcleo del sistema.

### 23.1 Módulo de usuarios

- inicio de sesión;
- roles;
- permisos;
- asignaciones docentes.

### 23.2 Módulo de estructura escolar

- ciclo lectivo;
- turnos;
- cursos;
- divisiones;
- materias;
- horarios.

### 23.3 Módulo de alumnos

- alta;
- baja;
- asignación a curso;
- historial de asignaciones.

### 23.4 Módulo docente

- mis cursos;
- mis alumnos;
- registro rápido de observaciones;
- historial propio.

### 23.5 Módulo directivo

- consulta transversal;
- búsqueda de alumnos;
- evolución;
- indicadores iniciales;
- solicitudes de seguimiento;
- intervenciones.

### 23.6 Auditoría

- registro de acciones sensibles;
- historial de modificaciones.

---

## 24. Lo que NO se implementará inicialmente

Para evitar que la primera versión se vuelva demasiado compleja, no se priorizarán inicialmente:

- inteligencia artificial predictiva;
- aplicación móvil nativa;
- integración con múltiples sistemas externos;
- analítica avanzada;
- automatizaciones complejas;
- modelos de riesgo clínico o psicológico;
- funcionamiento multiescuela.

Estas funciones podrán evaluarse después de validar el funcionamiento institucional básico.

---

## 25. Evolución posterior prevista

Si la primera versión funciona correctamente, el sistema podrá evolucionar hacia:

1. integración de asistencia;
2. integración más completa de calificaciones;
3. paneles de indicadores para dirección;
4. análisis temporal de trayectorias;
5. detección de patrones entre materias;
6. análisis estadístico institucional;
7. identificación sistemática de fortalezas y oportunidades;
8. notificaciones y flujos de seguimiento;
9. integración con otras herramientas institucionales;
10. aplicación móvil nativa, si el uso real demuestra que aporta valor.

---

## 26. Ciencia de datos como segunda etapa

La plataforma deberá construirse de manera que los datos históricos puedan utilizarse posteriormente para investigación y análisis estadístico, respetando las condiciones institucionales y legales correspondientes.

Una evolución posible sería:

```text
REGISTROS OPERATIVOS
        ↓
DATOS LIMPIOS Y ESTRUCTURADOS
        ↓
INDICADORES DESCRIPTIVOS
        ↓
ANÁLISIS ESTADÍSTICO
        ↓
DETECCIÓN DE PATRONES
        ↓
MODELOS PREDICTIVOS (eventualmente)
```

El desarrollo de modelos predictivos no forma parte del primer alcance y no deberá adelantarse al conocimiento suficiente de la calidad y significado de los datos.

---

## 27. Principios institucionales de diseño

El proyecto deberá mantenerse alineado con los siguientes principios:

### Simplicidad para el docente

Registrar debe requerir el menor esfuerzo posible.

### Contexto

Cada evento debe saber dónde, cuándo, con qué materia y bajo qué responsabilidad docente ocurrió.

### Privacidad

Cada usuario debe acceder solamente a la información necesaria para su función.

### Trazabilidad

Las acciones relevantes deben poder ser reconstruidas.

### No estigmatización

El sistema debe detectar señales, no etiquetar personas.

### Equilibrio

Deben registrarse tanto dificultades como fortalezas.

### Historial

Los cambios de año, curso y docentes no deben destruir la historia.

### Evolución progresiva

La plataforma debe comenzar con un núcleo simple y crecer sobre una arquitectura sólida.

### Decisión humana

Una alerta es una señal para revisar, no una decisión automática sobre el alumno.

---

## 28. Próximos documentos técnicos

A partir de este alcance, los siguientes documentos de diseño deberían ser elaborados en este orden:

1. **Modelo conceptual de entidades y relaciones.**
2. **Matriz de roles y permisos.**
3. **Catálogo inicial de eventos y observaciones.**
4. **Flujos de usuario de docentes y directivos.**
5. **Modelo de ciclo lectivo, altas, bajas y movimientos.**
6. **Diseño de la base de datos PostgreSQL.**
7. **Arquitectura inicial del proyecto Django.**
8. **Diseño de las primeras pantallas.**
9. **Plan de pruebas internas.**
10. **Plan de despliegue institucional.**

---

## 29. Decisiones consolidadas hasta la fecha

| Tema | Decisión actual |
|---|---|
| Institución | Escuela Secundaria N.º 63 |
| Turnos | Mañana y tarde |
| Entidad principal | Alumno |
| Tipo de solución | Sistema institucional de seguimiento |
| Acceso docente | Restringido a materias/cursos asignados |
| Visión global del alumno | Reservada a roles autorizados |
| Registro docente | Rápido, estructurado y contextualizado |
| Comentarios | Opcionales salvo situaciones que requieran contexto |
| Categorías | Definidas institucionalmente y ampliables por roles autorizados |
| Eventos positivos | Sí |
| Eventos de atención | Sí |
| Indicadores automáticos | Sí, como señales de revisión |
| Diagnóstico automático | No |
| Horario de clase | Se registra y valida contra asignaciones |
| Historial | Conservado entre ciclos y movimientos |
| Altas/bajas alumnos | Sí |
| Altas/bajas docentes | Sí |
| Suplencias | Sí |
| Ciclo lectivo | Parte estructural del modelo |
| Tecnología | Django + PostgreSQL + web responsive |
| Frontend inicial | Django Templates + HTML/CSS/JS |
| App nativa | No en la primera etapa |
| Análisis de datos | Etapa posterior |
| IA/ML | Etapa posterior, no necesaria para el MVP |
| Alcance inicial | Una sola escuela, preparada para adopción institucional completa |

---

## 30. Estado del proyecto

El proyecto se encuentra actualmente en una etapa de **definición conceptual y funcional**.

Ya existe una decisión tecnológica preliminar y un alcance institucional suficientemente definido para pasar al siguiente nivel de detalle: **modelar formalmente la información y las relaciones del sistema antes de comenzar la implementación**.

La siguiente etapa recomendada es diseñar el **modelo de entidades y relaciones (ER)** y, en paralelo, una primera **matriz de permisos por rol**. Estos dos elementos permitirán transformar la idea institucional en una arquitectura de software concreta.
