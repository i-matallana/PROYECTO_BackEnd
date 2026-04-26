from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Entrenador
from app.schemas.schemas import EntrenadorCreate, EntrenadorRead

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

@router.get("/", response_model=list[EntrenadorRead])
def listar_entrenadores(db: Session = Depends(get_db)):
    return db.query(Entrenador).all()

@router.get("/{id_entrenador}", response_model=EntrenadorRead)
def obtener_entrenador(id_entrenador: str, db: Session = Depends(get_db)):
    entrenador = db.query(Entrenador).filter(Entrenador.id_entrenador == id_entrenador).first()
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador

@router.post("/", response_model=EntrenadorRead)
def crear_entrenador(datos: EntrenadorCreate, db: Session = Depends(get_db)):
    existe = db.query(Entrenador).filter(Entrenador.id_entrenador == datos.id_entrenador).first()
    if existe:
        raise HTTPException(status_code=400, detail="El entrenador ya existe")
    nuevo = Entrenador(
        id_entrenador  = datos.id_entrenador,
        anhos_exp      = datos.anhos_exp,
        id_instalacion = datos.id_instalacion
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_entrenador}", response_model=EntrenadorRead)
def actualizar_entrenador(id_entrenador: str, datos: EntrenadorCreate, db: Session = Depends(get_db)):
    entrenador = db.query(Entrenador).filter(Entrenador.id_entrenador == id_entrenador).first()
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    entrenador.anhos_exp      = datos.anhos_exp
    entrenador.id_instalacion = datos.id_instalacion
    db.commit()
    db.refresh(entrenador)
    return entrenador

@router.delete("/{id_entrenador}")
def eliminar_entrenador(id_entrenador: str, db: Session = Depends(get_db)):
    entrenador = db.query(Entrenador).filter(Entrenador.id_entrenador == id_entrenador).first()
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    db.delete(entrenador)
    db.commit()
    return {"mensaje": f"Entrenador {id_entrenador} eliminado correctamente"}
