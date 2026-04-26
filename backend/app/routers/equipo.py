from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Equipo
from app.schemas.schemas import EquipoCreate, EquipoRead

router = APIRouter(prefix="/equipos", tags=["Equipos"])

@router.get("/", response_model=list[EquipoRead])
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(Equipo).all()

@router.get("/{id_equipo}", response_model=EquipoRead)
def obtener_equipo(id_equipo: str, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter(Equipo.id_equipo == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@router.post("/", response_model=EquipoRead)
def crear_equipo(datos: EquipoCreate, db: Session = Depends(get_db)):
    existe = db.query(Equipo).filter(Equipo.id_equipo == datos.id_equipo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El equipo ya existe")
    nuevo = Equipo(
        id_equipo  = datos.id_equipo,
        nomEqui    = datos.nomEqui,
        cant_int   = datos.cant_int,
        cat_gen    = datos.cat_gen,
        cat_edad   = datos.cat_edad,
        id_deporte = datos.id_deporte
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_equipo}", response_model=EquipoRead)
def actualizar_equipo(id_equipo: str, datos: EquipoCreate, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter(Equipo.id_equipo == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    equipo.nomEqui    = datos.nomEqui
    equipo.cant_int   = datos.cant_int
    equipo.cat_gen    = datos.cat_gen
    equipo.cat_edad   = datos.cat_edad
    equipo.id_deporte = datos.id_deporte
    db.commit()
    db.refresh(equipo)
    return equipo

@router.delete("/{id_equipo}")
def eliminar_equipo(id_equipo: str, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter(Equipo.id_equipo == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    db.delete(equipo)
    db.commit()
    return {"mensaje": f"Equipo {id_equipo} eliminado correctamente"}
