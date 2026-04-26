from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Instalacion
from app.schemas.schemas import InstalacionCreate, InstalacionRead

router = APIRouter(prefix="/instalaciones", tags=["Instalaciones"])

@router.get("/", response_model=list[InstalacionRead])
def listar_instalaciones(db: Session = Depends(get_db)):
    return db.query(Instalacion).all()

@router.get("/{id_instalacion}", response_model=InstalacionRead)
def obtener_instalacion(id_instalacion: str, db: Session = Depends(get_db)):
    inst = db.query(Instalacion).filter(Instalacion.id_instalacion == id_instalacion).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    return inst

@router.post("/", response_model=InstalacionRead)
def crear_instalacion(datos: InstalacionCreate, db: Session = Depends(get_db)):
    existe = db.query(Instalacion).filter(Instalacion.id_instalacion == datos.id_instalacion).first()
    if existe:
        raise HTTPException(status_code=400, detail="La instalación ya existe")
    nueva = Instalacion(
        id_instalacion = datos.id_instalacion,
        nomInst        = datos.nomInst,
        id_zona        = datos.id_zona
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{id_instalacion}", response_model=InstalacionRead)
def actualizar_instalacion(id_instalacion: str, datos: InstalacionCreate, db: Session = Depends(get_db)):
    inst = db.query(Instalacion).filter(Instalacion.id_instalacion == id_instalacion).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    inst.nomInst = datos.nomInst
    inst.id_zona = datos.id_zona
    db.commit()
    db.refresh(inst)
    return inst

@router.delete("/{id_instalacion}")
def eliminar_instalacion(id_instalacion: str, db: Session = Depends(get_db)):
    inst = db.query(Instalacion).filter(Instalacion.id_instalacion == id_instalacion).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    db.delete(inst)
    db.commit()
    return {"mensaje": f"Instalación {id_instalacion} eliminada correctamente"}