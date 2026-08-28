FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production

WORKDIR /app

# Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Estáticos
# Los secretos reales (SECRET_KEY, DB_*) se inyectan en runtime vía EasyPanel.
# Estos valores placeholder solo permiten ejecutar collectstatic durante el
# build (no son secretos y no se usan en producción).
RUN SECRET_KEY=build-only-not-a-secret \
    DB_NAME=dummy DB_USER=dummy DB_PASSWORD=dummy DB_HOST=dummy \
    python manage.py collectstatic --noinput

# Puerto (EasyPanel usa 80 por defecto)
EXPOSE 80

# Gunicorn con 2 workers y timeout amplio
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "120"]
