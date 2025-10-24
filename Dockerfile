FROM python:3.9-slim

WORKDIR /app

# Copia el archivo de dependencias desde el contexto de build (la raíz del proyecto)
# Esto se hace primero para aprovechar la caché de Docker. Si requirements.txt no cambia,
# Docker no volverá a instalar las dependencias.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación desde el contexto de build
COPY . .

EXPOSE 8000