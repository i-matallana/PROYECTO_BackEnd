from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Horario
from app.schemas.schemas import HorarioCreate, HorarioRead

router = APIRouter(prefix="/horarios", tags=["Horarios"])

@router.get("/", response_model=list[HorarioRead])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(Horario).all()

@router.get("/{id_horario}", response_model=HorarioRead)
def obtener_horario(id_horario: str, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

@router.post("/", response_model=HorarioRead)
def crear_horario(datos: HorarioCreate, db: Session = Depends(get_db)):
    existe = db.query(Horario).filter(Horario.id_horario == datos.id_horario).first()
    if existe:
        raise HTTPException(status_code=400, detail="El horario ya existe")
    nuevo = Horario(
        id_horario     = datos.id_horario,
        dias           = datos.dias,
        hora_ini       = datos.hora_ini,
        hora_fin       = datos.hora_fin,
        id_instalacion = datos.id_instalacion
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_horario}", response_model=HorarioRead)
def actualizar_horario(id_horario: str, datos: HorarioCreate, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    horario.dias           = datos.dias
    horario.hora_ini       = datos.hora_ini
    horario.hora_fin       = datos.hora_fin
    horario.id_instalacion = datos.id_instalacion
    db.commit()
    db.refresh(horario)
    return horario

@router.delete("/{id_horario}")
def eliminar_horario(id_horario: str, db: Session = Depends(get_db)):
    horario = db.query(Horario).filter(Horario.id_horario == id_horario).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    db.delete(horario)
    db.commit()
    return {"mensaje": f"Horario {id_horario} eliminado correctamente"}