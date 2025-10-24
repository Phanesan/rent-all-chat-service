FROM python:3.9-slim

WORKDIR /app

# Copia el archivo de dependencias desde el directorio padre (el contexto de build)
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación desde el directorio padre
COPY .. .

EXPOSE 8080