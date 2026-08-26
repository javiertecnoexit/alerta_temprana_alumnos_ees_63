from django.utils import timezone


def es_dentro_de_horario(asignacion_docente, fecha_hora):
    """
    Determina si fecha_hora está dentro del horario de la asignación.

    La asignación tiene horarios relacionados (related_name='horarios'),
    cada uno con dia_semana, hora_inicio, hora_fin.

    Reglas:
    - Obtener el día de la semana de fecha_hora (lunes..viernes)
    - Buscar horarios de la asignación para ese día
    - Si hay horario y la hora de fecha_hora está entre
      hora_inicio y hora_fin → True
    - Si es sábado/domingo → False
    - Si no hay horario para ese día → False
    """
    # Mapear weekday de Python (0=lunes..6=domingo) a TextChoices
    dia_map = {
        0: "lunes",
        1: "martes",
        2: "miercoles",
        3: "jueves",
        4: "viernes",
    }
    weekday = fecha_hora.weekday()
    if weekday not in dia_map:
        return False
    dia = dia_map[weekday]

    horarios = asignacion_docente.horarios.filter(dia_semana=dia)
    hora_actual = fecha_hora.time()

    for horario in horarios:
        if horario.hora_inicio <= hora_actual <= horario.hora_fin:
            return True
    return False