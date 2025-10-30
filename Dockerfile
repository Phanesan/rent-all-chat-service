# Usa una imagen oficial de Python
FROM python:3.12-alpine

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de dependencias y las instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Crea el directorio de logs
RUN mkdir logs

# Expone el puerto en el que se ejecuta la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
