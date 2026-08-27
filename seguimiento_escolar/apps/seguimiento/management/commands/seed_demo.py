from datetime import date, time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import (
    AsignacionDocente,
    Curso,
    Horario,
    Materia,
    Turno,
)
from apps.observaciones.models import CatalogoObservacion, Observacion
from apps.seguimiento.models import PreceptorTurno

CONTRASENA_DEMO = "Demo1234"


class Command(BaseCommand):
    help = "Carga datos ficticios de demostración para el sistema ES63"

    def handle(self, *args, **options):
        # Idempotente: si ya existe el ciclo 2026, abortar
        if CicloLectivo.objects.filter(anio=2026).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Ya existen datos demo. No se hace nada."
                )
            )
            return

        User = get_user_model()

        # 1. Ciclo lectivo 2026 (activo)
        ciclo = CicloLectivo.objects.create(
            anio=2026,
            fecha_inicio=date(2026, 3, 2),
            fecha_fin=date(2026, 11, 27),
            estado=CicloLectivo.Estado.ACTIVO,
            activo=True,
        )

        # 2. Turnos
        turno_manana, _ = Turno.objects.get_or_create(
            nombre=Turno.Nombre.MANANA
        )
        turno_tarde, _ = Turno.objects.get_or_create(
            nombre=Turno.Nombre.TARDE
        )

        # 3. Cursos (3 por turno)
        cursos_manana = []
        cursos_tarde = []
        for anio in (1, 2, 3):
            cursos_manana.append(
                Curso.objects.create(
                    anio=anio,
                    division="A",
                    turno=turno_manana,
                    ciclo_lectivo=ciclo,
                )
            )
            cursos_tarde.append(
                Curso.objects.create(
                    anio=anio,
                    division="B",
                    turno=turno_tarde,
                    ciclo_lectivo=ciclo,
                )
            )
        cursos = cursos_manana + cursos_tarde

        # 4. Materias
        materias_nombres = [
            "Matemática",
            "Lengua",
            "Historia",
            "Biología",
            "Inglés",
            "Educación Física",
        ]
        materias = {
            nombre: Materia.objects.create(nombre=nombre)
            for nombre in materias_nombres
        }

        # 5. Usuarios (por rol)
        admin_demo, _ = User.objects.get_or_create(
            username="admin_demo",
            defaults={"rol": User.Rol.ADMIN},
        )
        admin_demo.rol = User.Rol.ADMIN
        admin_demo.is_staff = True
        admin_demo.is_superuser = True
        admin_demo.set_password(CONTRASENA_DEMO)
        admin_demo.save()

        directivo1, _ = User.objects.get_or_create(
            username="directivo1",
            defaults={"rol": User.Rol.DIRECTIVO},
        )
        directivo1.set_password(CONTRASENA_DEMO)
        directivo1.save()

        preceptor_manana, _ = User.objects.get_or_create(
            username="preceptor_manana",
            defaults={"rol": User.Rol.PRECEPTOR},
        )
        preceptor_manana.set_password(CONTRASENA_DEMO)
        preceptor_manana.save()
        PreceptorTurno.objects.get_or_create(
            preceptor=preceptor_manana, turno=turno_manana
        )

        preceptor_tarde, _ = User.objects.get_or_create(
            username="preceptor_tarde",
            defaults={"rol": User.Rol.PRECEPTOR},
        )
        preceptor_tarde.set_password(CONTRASENA_DEMO)
        preceptor_tarde.save()
        PreceptorTurno.objects.get_or_create(
            preceptor=preceptor_tarde, turno=turno_tarde
        )

        docente_mat, _ = User.objects.get_or_create(
            username="docente_mat",
            defaults={"rol": User.Rol.DOCENTE},
        )
        docente_mat.set_password(CONTRASENA_DEMO)
        docente_mat.save()

        docente_leng, _ = User.objects.get_or_create(
            username="docente_leng",
            defaults={"rol": User.Rol.DOCENTE},
        )
        docente_leng.set_password(CONTRASENA_DEMO)
        docente_leng.save()

        docente_hist, _ = User.objects.get_or_create(
            username="docente_hist",
            defaults={"rol": User.Rol.DOCENTE},
        )
        docente_hist.set_password(CONTRASENA_DEMO)
        docente_hist.save()

        # 6. Asignaciones docentes (titulares)
        asignaciones = []

        # docente_mat → Matemática en 1°A, 2°A, 3°A (mañana)
        for curso in cursos_manana:
            asignaciones.append(
                AsignacionDocente.objects.create(
                    docente=docente_mat,
                    materia=materias["Matemática"],
                    curso=curso,
                    tipo=AsignacionDocente.Tipo.TITULAR,
                    fecha_inicio=date(2026, 3, 2),
                    activa=True,
                )
            )

        # docente_leng → Lengua en 1°A, 2°A, 3°A (mañana)
        for curso in cursos_manana:
            asignaciones.append(
                AsignacionDocente.objects.create(
                    docente=docente_leng,
                    materia=materias["Lengua"],
                    curso=curso,
                    tipo=AsignacionDocente.Tipo.TITULAR,
                    fecha_inicio=date(2026, 3, 2),
                    activa=True,
                )
            )

        # docente_hist → Historia en 1°B, 2°B, 3°B (tarde)
        for curso in cursos_tarde:
            asignaciones.append(
                AsignacionDocente.objects.create(
                    docente=docente_hist,
                    materia=materias["Historia"],
                    curso=curso,
                    tipo=AsignacionDocente.Tipo.TITULAR,
                    fecha_inicio=date(2026, 3, 2),
                    activa=True,
                )
            )

        # 7. Horarios para cada asignación (lunes y miércoles)
        total_horarios = 0
        for asignacion in asignaciones:
            for dia in (Horario.DiaSemana.LUNES, Horario.DiaSemana.MIERCOLES):
                Horario.objects.create(
                    asignacion_docente=asignacion,
                    dia_semana=dia,
                    hora_inicio=time(8, 0),
                    hora_fin=time(9, 0),
                )
                total_horarios += 1

        # 8. Alumnos ficticios (2-3 por curso)
        nombres_alumnos = [
            ("Juan", "Pérez"),
            ("María", "González"),
            ("Pedro", "López"),
            ("Ana", "Rodríguez"),
            ("Luis", "Fernández"),
            ("Carla", "Martínez"),
            ("Diego", "Sánchez"),
            ("Sofía", "Romero"),
            ("Nicolás", "Torres"),
            ("Valentina", "Ruiz"),
            ("Facundo", "Álvarez"),
            ("Camila", "Díaz"),
        ]
        total_alumnos = 0
        alumnos_curso = {}
        dni_base = 40111200
        for curso in cursos:
            # 2 alumnos por curso = 12 alumnos en total
            alumnos_del_curso = []
            for i in range(2):
                nombre, apellido = nombres_alumnos[total_alumnos]
                alumno = Alumno.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    dni=str(dni_base + total_alumnos),
                    fecha_nacimiento=date(2010, 1, 1),
                    estado=Alumno.Estado.ACTIVO,
                )
                alumnos_del_curso.append(alumno)
                total_alumnos += 1
            alumnos_curso[curso.id] = alumnos_del_curso

        # 9. AsignacionAlumnoCurso (condicion regular)
        for curso in cursos:
            for alumno in alumnos_curso[curso.id]:
                AsignacionAlumnoCurso.objects.create(
                    alumno=alumno,
                    curso=curso,
                    ciclo_lectivo=ciclo,
                    fecha_inicio=date(2026, 3, 2),
                    condicion=AsignacionAlumnoCurso.Condicion.REGULAR,
                    activa=True,
                )

        # 10. Observaciones de ejemplo (usar categorías del catálogo)
        # El fixture catalogo_observaciones.json ya cargó las 27 categorías.
        catalogo_positivo = CatalogoObservacion.objects.filter(
            nombre="Participación destacada"
        ).first() or CatalogoObservacion.objects.first()
        catalogo_atencion = CatalogoObservacion.objects.filter(
            nombre="No completa la actividad"
        ).first() or CatalogoObservacion.objects.first()
        catalogo_neutro = CatalogoObservacion.objects.filter(
            nombre="No dispone del material necesario"
        ).first() or CatalogoObservacion.objects.first()

        primer_curso_manana = cursos_manana[0]
        primer_alumno = alumnos_curso[primer_curso_manana.id][0]
        segundo_alumno = alumnos_curso[primer_curso_manana.id][1]

        Observacion.objects.create(
            alumno=primer_alumno,
            docente=docente_mat,
            materia=materias["Matemática"],
            curso=primer_curso_manana,
            catalogo=catalogo_positivo,
            ciclo_lectivo=ciclo,
            fecha_hora=timezone.make_aware(timezone.datetime(2026, 4, 15, 9, 0)),
            turno=turno_manana.nombre,
            comentario="Participa activamente en clase",
        )
        Observacion.objects.create(
            alumno=segundo_alumno,
            docente=docente_mat,
            materia=materias["Matemática"],
            curso=primer_curso_manana,
            catalogo=catalogo_atencion,
            ciclo_lectivo=ciclo,
            fecha_hora=timezone.make_aware(timezone.datetime(2026, 4, 15, 9, 0)),
            turno=turno_manana.nombre,
            comentario="No completó la actividad de la clase",
        )
        Observacion.objects.create(
            alumno=primer_alumno,
            docente=docente_leng,
            materia=materias["Lengua"],
            curso=primer_curso_manana,
            catalogo=catalogo_neutro,
            ciclo_lectivo=ciclo,
            fecha_hora=timezone.make_aware(timezone.datetime(2026, 4, 15, 9, 0)),
            turno=turno_manana.nombre,
            comentario="No trajo el libro de lectura",
        )

        # Resumen
        self.stdout.write(self.style.SUCCESS("Datos demo cargados:"))
        self.stdout.write("  Ciclos: 1")
        self.stdout.write("  Turnos: 2")
        self.stdout.write(f"  Cursos: {len(cursos)}")
        self.stdout.write(f"  Materias: {len(materias)}")
        self.stdout.write("  Usuarios: 6")
        self.stdout.write(f"  Asignaciones docentes: {len(asignaciones)}")
        self.stdout.write(f"  Horarios: {total_horarios}")
        self.stdout.write(f"  Alumnos: {total_alumnos}")
        self.stdout.write("  Observaciones: 3")
        self.stdout.write(
            f"  Usuarios demo: docente_mat, docente_leng, docente_hist, "
            f"preceptor_manana, preceptor_tarde, directivo1 / {CONTRASENA_DEMO}"
        )