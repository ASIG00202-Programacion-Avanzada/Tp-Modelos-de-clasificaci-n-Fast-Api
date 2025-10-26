# 1. Imagen base
FROM python:3.11-slim

# 2. Crear directorio de trabajo
WORKDIR /app

# 3. Copiar requirements y código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 4. Exponer puerto y comando
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
