from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Inicializar app
app = FastAPI()

# Middleware CORS - DEBE IR ANTES DE LAS RUTAS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# -----------------------------
# MODELOS
# -----------------------------
class Marker(BaseModel):
    lat: float
    lon: float
    tipo_incidente: str
    descripcion: str
    hora_suceso: str
    notas: Optional[str] = ""

class MarkerResponse(BaseModel):
    id: int
    lat: float
    lon: float
    tipo_incidente: str
    descripcion: str
    hora_suceso: str
    notas: Optional[str]
    fecha_creacion: str

# -----------------------------
# BASE DE DATOS EN MEMORIA (temporal)
# -----------------------------
marcadores_db = []
next_id = 1

# -----------------------------
# RUTAS
# -----------------------------

@app.get("/")
def home():
    return {"mensaje": "API de GeoSafe funcionando correctamente ✅"}

@app.options("/{path:path}")
async def options_handler(path: str):
    return {"message": "OK"}

@app.get("/markers")
def get_markers():
    """Obtiene todos los marcadores guardados."""
    return marcadores_db

@app.post("/markers")
def add_marker(marker: Marker):
    """Agrega un nuevo marcador."""
    global next_id
    
    nuevo_marcador = {
        "id": next_id,
        "lat": marker.lat,
        "lon": marker.lon,
        "tipo_incidente": marker.tipo_incidente,
        "descripcion": marker.descripcion,
        "hora_suceso": marker.hora_suceso,
        "notas": marker.notas if marker.notas else "",
        "fecha_creacion": datetime.now().isoformat()
    }
    
    marcadores_db.append(nuevo_marcador)
    next_id += 1
    
    return {
        "mensaje": "Marcador agregado correctamente", 
        "id": nuevo_marcador["id"],
        "marker": nuevo_marcador
    }

@app.delete("/markers/{marker_id}")
def delete_marker(marker_id: int):
    """Elimina un marcador por ID."""
    global marcadores_db
    
    # Buscar el marcador
    marcador_encontrado = None
    for m in marcadores_db:
        if m["id"] == marker_id:
            marcador_encontrado = m
            break
    
    if not marcador_encontrado:
        raise HTTPException(status_code=404, detail="Marcador no encontrado")
    
    # Eliminar el marcador
    marcadores_db = [m for m in marcadores_db if m["id"] != marker_id]
    
    return {"status": "deleted", "id": marker_id}
