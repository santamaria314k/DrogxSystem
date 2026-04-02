# ── Imagen base ──────────────────────────────────────────────
FROM python:3.11-slim

# ── Variables de entorno ──────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── Directorio de trabajo ─────────────────────────────────────
WORKDIR /app

# ── Dependencias del sistema ──────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ── Dependencias Python ───────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Código fuente ─────────────────────────────────────────────
COPY . .

# ── Puerto expuesto ───────────────────────────────────────────
EXPOSE 8000

# ── Comando por defecto (sobreescrito en docker-compose) ──────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
