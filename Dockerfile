# Imagen base
FROM python:3.13-slim

# Carpeta de trabajo
WORKDIR /app

# Instalar librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY vigilante.py .

# Comando de arranque (Python correrá en bucle infinito)
CMD ["python", "vigilante.py"]