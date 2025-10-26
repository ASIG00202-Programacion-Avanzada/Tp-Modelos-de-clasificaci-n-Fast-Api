

# Instalacion y uso del proyecto


# Crear entorno virtual
- python3 -m venv venv

# Activar entorno virtual
# Linux/macOS
- source venv/bin/activate
# Windows
- venv\Scripts\activate

# Instalar dependencias
- pip install -r requirements.txt

# Levantar API
- uvicorn src.app:app --reload
- Entrar a localhost:8000/docs