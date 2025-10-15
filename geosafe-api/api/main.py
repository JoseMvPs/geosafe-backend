from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .db import get_db
from .models import Point

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add_point")
def add_point(p: Point):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO puntos (lat, lng) VALUES (%s, %s)", (p.lat, p.lng))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/get_points", response_model=List[Point])
def get_points():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT lat, lng FROM puntos ORDER BY fecha DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

