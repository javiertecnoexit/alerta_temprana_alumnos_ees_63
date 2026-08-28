from django import forms

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import (
    AsignacionDocente,
    Curso,
    Horario,
    Materia,
    Turno,
)
from apps.usuarios.models import Usuario


class AlumnoForm(forms.ModelForm):
    """Formulario de alta/edición de un alumno."""

    curso = forms.ModelChoiceField(
        queryset=Curso.objects.filter(activo=True),
        required=False,
        label="Curso (asignación)",
        help_text="Opcional: al crear el alumno lo asigna a un curso.",
    )
    ciclo_lectivo = forms.ModelChoiceField(
        queryset=CicloLectivo.objects.filter(activo=True),
        required=False,
        label="Ciclo lectivo (asignación)",
        help_text="Opcional: ciclo lectivo de la asignación del alumno.",
    )

    class Meta:
        model = Alumno
        fields = ["nombre", "apellido", "dni", "fecha_nacimiento", "estado"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date", "class": "form-control"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        # La asignación de curso solo aplica al alta, no a la edición
        if self.instance and self.instance.pk:
            for campo in ("curso", "ciclo_lectivo"):
                self.fields.pop(campo)

    def clean(self):
        cleaned = super().clean()
        curso = cleaned.get("curso")
        ciclo_lectivo = cleaned.get("ciclo_lectivo")
        if bool(curso) != bool(ciclo_lectivo):
            raise forms.ValidationError(
                "Para asignar un curso debe indicarse también el ciclo lectivo "
                "(y viceversa)."
            )
        return cleaned


class DocenteForm(forms.ModelForm):
    """Formulario de alta/edición de un docente (Usuario con rol docente)."""

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        help_text="Solo se completa al crear; dejar vacío al editar para no cambiar.",
    )

    class Meta:
        model = Usuario
        fields = ["username", "first_name", "last_name", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        # En edición la contraseña no es obligatoria
        if self.instance and self.instance.pk:
            self.fields["password"].required = False

    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = Usuario.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre de usuario.")
        return username

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = Usuario.Rol.DOCENTE
        password = self.cleaned_data.get("password")
        if password:
            usuario.set_password(password)
        # Al editar nunca se debe desactivar desde este formulario
        if commit:
            usuario.save()
        return usuario


class _BaseFormMixin:
    """Mixin para aplicar la clase form-control a todos los campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class MateriaForm(_BaseFormMixin, forms.ModelForm):
    """Formulario de alta/edición de una materia."""

    class Meta:
        model = Materia
        fields = ["nombre", "activa"]


class TurnoForm(_BaseFormMixin, forms.ModelForm):
    """Formulario de alta/edición de un turno."""

    class Meta:
        model = Turno
        fields = ["nombre", "activo"]


class CursoForm(_BaseFormMixin, forms.ModelForm):
    """Formulario de alta/edición de un curso."""

    class Meta:
        model = Curso
        fields = ["anio", "division", "turno", "ciclo_lectivo", "activo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["turno"].queryset = Turno.objects.filter(activo=True)
        self.fields["ciclo_lectivo"].queryset = CicloLectivo.objects.filter(
            activo=True
        )


class CicloLectivoForm(_BaseFormMixin, forms.ModelForm):
    """Formulario de alta/edición de un ciclo lectivo."""

    class Meta:
        model = CicloLectivo
        fields = ["anio", "fecha_inicio", "fecha_fin", "estado", "activo"]
        widgets = {
            "fecha_inicio": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "fecha_fin": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }


class AsignacionDocenteForm(_BaseFormMixin, forms.ModelForm):
    """Formulario de alta/edición de una asignación docente."""

    class Meta:
        model = AsignacionDocente
        fields = [
            "docente",
            "materia",
            "curso",
            "tipo",
            "fecha_inicio",
            "fecha_fin",
            "activa",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "fecha_fin": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["docente"].queryset = Usuario.objects.filter(
            rol=Usuario.Rol.DOCENTE, is_active=True
        )
        self.fields["curso"].queryset = Curso.objects.filter(activo=True)


class AsignacionAlumnoCursoForm(_BaseFormMixin, forms.ModelForm):
    """Formulario de alta/edición de una asignación alumno-curso."""

    class Meta:
        model = AsignacionAlumnoCurso
        fields = [
            "alumno",
            "curso",
            "ciclo_lectivo",
            "fecha_inicio",
            "fecha_fin",
            "condicion",
            "activa",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "fecha_fin": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["alumno"].queryset = Alumno.objects.filter(
            estado=Alumno.Estado.ACTIVO
        ).order_by("apellido", "nombre")
        self.fields["curso"].queryset = Curso.objects.filter(activo=True)
        self.fields["ciclo_lectivo"].queryset = CicloLectivo.objects.filter(
            activo=True
        )


class HorarioForm(_BaseFormMixin, forms.ModelForm):
    """Formulario de alta/edición de un horario de asignación docente."""

    class Meta:
        model = Horario
        fields = [
            "asignacion_docente",
            "dia_semana",
            "hora_inicio",
            "hora_fin",
        ]
        widgets = {
            "hora_inicio": forms.TimeInput(
                format="%H:%M",
                attrs={"type": "time"},
            ),
            "hora_fin": forms.TimeInput(
                format="%H:%M",
                attrs={"type": "time"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["asignacion_docente"].queryset = (
            AsignacionDocente.objects.filter(activa=True).select_related(
                "docente", "materia", "curso"
            )
        )
