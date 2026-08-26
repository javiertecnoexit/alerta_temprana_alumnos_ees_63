from django import forms

from apps.alumnos.models import Alumno

from .models import Intervencion, SolicitudInfo


class SolicitudInfoForm(forms.ModelForm):
    class Meta:
        model = SolicitudInfo
        fields = ["alumno", "motivo"]
        widgets = {
            "alumno": forms.Select,
            "motivo": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": (
                        "Indicá el motivo de la solicitud de información "
                        "sobre el alumno."
                    ),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # El docente solo puede solicitar información de alumnos de sus cursos
        if user is not None:
            from apps.estructura_escolar.models import AsignacionDocente

            alumno_ids = (
                AsignacionDocente.objects.filter(docente=user, activa=True)
                .values_list("curso_id", flat=True)
            )
            self.fields["alumno"].queryset = Alumno.objects.filter(
                asignaciones_curso__curso_id__in=alumno_ids
            ).distinct().order_by("apellido", "nombre")


class RespuestaSolicitudForm(forms.ModelForm):
    class Meta:
        model = SolicitudInfo
        fields = ["estado", "respuesta"]
        widgets = {
            "estado": forms.Select(
                choices=[
                    (SolicitudInfo.Estado.RESPONDIDA, "Respondida"),
                    (SolicitudInfo.Estado.RECHAZADA, "Rechazada"),
                ]
            ),
            "respuesta": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Detalle de la respuesta"}
            ),
        }


class IntervencionForm(forms.ModelForm):
    class Meta:
        model = Intervencion
        fields = ["tipo", "descripcion"]
        widgets = {
            "tipo": forms.Select,
            "descripcion": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Descripción de la intervención realizada",
                }
            ),
        }