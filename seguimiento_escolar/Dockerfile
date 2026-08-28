FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Estáticos
RUN python manage.py collectstatic --noinput

# Puerto (EasyPanel usa 80 por defecto)
EXPOSE 80

# Gunicorn con 2 workers y timeout amplio
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "120"]
