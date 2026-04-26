from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Zona
from app.schemas.schemas import ZonaCreate, ZonaRead

router = APIRouter(prefix="/zonas", tags=["Zonas"])

@router.get("/", response_model=list[ZonaRead])
def listar_zonas(db: Session = Depends(get_db)):
    return db.query(Zona).all()

@router.get("/{id_zona}", response_model=ZonaRead)
def obtener_zona(id_zona: str, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id_zona == id_zona).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zona

@router.post("/", response_model=ZonaRead)
def crear_zona(datos: ZonaCreate, db: Session = Depends(get_db)):
    existe = db.query(Zona).filter(Zona.id_zona == datos.id_zona).first()
    if existe:
        raise HTTPException(status_code=400, detail="La zona ya existe")
    nueva = Zona(
        id_zona   = datos.id_zona,
        nomZona   = datos.nomZona,
        municipio = datos.municipio
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{id_zona}", response_model=ZonaRead)
def actualizar_zona(id_zona: str, datos: ZonaCreate, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id_zona == id_zona).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    zona.nomZona   = datos.nomZona
    zona.municipio = datos.municipio
    db.commit()
    db.refresh(zona)
    return zona

@router.delete("/{id_zona}")
def eliminar_zona(id_zona: str, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id_zona == id_zona).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    db.delete(zona)
    db.commit()
    return {"mensaje": f"Zona {id_zona} eliminada correctamente"}