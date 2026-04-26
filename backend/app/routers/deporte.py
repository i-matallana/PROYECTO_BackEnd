from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Deporte
from app.schemas.schemas import DeporteCreate, DeporteRead

router = APIRouter(prefix="/deportes", tags=["Deportes"])


# ── GET todos ─────────────────────────────────────────
@router.get("/", response_model=list[DeporteRead])
def listar_deportes(db: Session = Depends(get_db)):
    return db.query(Deporte).all()


# ── GET por ID ────────────────────────────────────────
@router.get("/{id_deporte}", response_model=DeporteRead)
def obtener_deporte(id_deporte: str, db: Session = Depends(get_db)):
    deporte = db.query(Deporte).filter(Deporte.id_deporte == id_deporte).first()
    if not deporte:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    return deporte


# ── POST crear ────────────────────────────────────────
@router.post("/", response_model=DeporteRead)
def crear_deporte(datos: DeporteCreate, db: Session = Depends(get_db)):
    existe = db.query(Deporte).filter(Deporte.id_deporte == datos.id_deporte).first()
    if existe:
        raise HTTPException(status_code=400, detail="El deporte ya existe")

    nuevo = Deporte(
        id_deporte = datos.id_deporte,
        nomDepo    = datos.nomDepo
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ── PUT actualizar ────────────────────────────────────
@router.put("/{id_deporte}", response_model=DeporteRead)
def actualizar_deporte(id_deporte: str, datos: DeporteCreate, db: Session = Depends(get_db)):
    deporte = db.query(Deporte).filter(Deporte.id_deporte == id_deporte).first()
    if not deporte:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")

    deporte.nomDepo = datos.nomDepo

    db.commit()
    db.refresh(deporte)
    return deporte


# ── DELETE eliminar ───────────────────────────────────
@router.delete("/{id_deporte}")
def eliminar_deporte(id_deporte: str, db: Session = Depends(get_db)):
    deporte = db.query(Deporte).filter(Deporte.id_deporte == id_deporte).first()
    if not deporte:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")

    db.delete(deporte)
    db.commit()
    return {"mensaje": f"Deporte {id_deporte} eliminado correctamente"}