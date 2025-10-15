from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Inicializar la app FastAPI
app = FastAPI()

# Permitir peticiones desde tu frontend (ajusta el dominio si es necesario)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner tu dominio de frontend aquí
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Obtener la URL de la base de datos desde las variables de entorno (en Vercel)
DATABASE_URL = os.getenv("DATABASE_URL")

# Función para conectar a la base de datos
def get_db_connection():
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL no configurada.")
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando a la base de datos: {e}")

# Ruta raíz (para probar que funciona el backend)
@app.get("/")
def root():
    return {"message": "🚀 API de GeoSafe funcionando correctamente en Vercel!"}


# Simulando base de datos en memoria
marcadores = []

class Marker(BaseModel):
    lat: float
    lon: float
    nombre: str

@app.get("/markers")
def obtener_marcadores():
    return marcadores

@app.post("/markers")
def agregar_marcador(marker: Marker):
    marcadores.append(marker)
    return {"mensaje": "Marcador agregado correctamente", "marker": marker}

