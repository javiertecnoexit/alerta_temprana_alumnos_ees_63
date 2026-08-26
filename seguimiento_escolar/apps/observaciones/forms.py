from django import forms

from .models import CatalogoObservacion, Observacion


class ObservacionForm(forms.ModelForm):
    class Meta:
        model = Observacion
        fields = ["catalogo", "comentario"]
        widgets = {
            "catalogo": forms.RadioSelect,
            "comentario": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Comentario opcional (contexto adicional)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo categorías activas
        self.fields["catalogo"].queryset = CatalogoObservacion.objects.filter(
            activo=True
        ).order_by("familia", "nombre")
        self.fields["comentario"].required = False