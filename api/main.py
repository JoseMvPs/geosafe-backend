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

# Ejemplo: obtener todos los registros de una tabla
@app.get("/usuarios")
def get_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM usuarios;")
        rows = cur.fetchall()
        return {"usuarios": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {e}")
    finally:
        cur.close()
        conn.close()

# Ejemplo: agregar un usuario
@app.post("/usuarios")
def add_usuario(nombre: str, email: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id;", (nombre, email))
        new_id = cur.fetchone()["id"]
        conn.commit()
        return {"message": "Usuario agregado con éxito", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar usuario: {e}")
    finally:
        cur.close()
        conn.close()
