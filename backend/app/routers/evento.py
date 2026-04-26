from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Evento
from app.schemas.schemas import EventoCreate, EventoRead
import uuid

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.get("/", response_model=list[EventoRead])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()

@router.get("/{id_evento}", response_model=EventoRead)
def obtener_evento(id_evento: str, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id_evento == id_evento).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

@router.post("/", response_model=EventoRead)
def crear_evento(datos: EventoCreate, db: Session = Depends(get_db)):
    nuevo = Evento(
        id_evento      = str(uuid.uuid4())[:20],
        nomEve         = datos.nomEve,
        fecha_ini      = datos.fecha_ini,
        fecha_fin      = datos.fecha_fin,
        descripcion    = datos.descripcion,
        id_deporte     = datos.id_deporte,
        id_instalacion = datos.id_instalacion,
        id_usuario     = datos.id_usuario
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id_evento}", response_model=EventoRead)
def actualizar_evento(id_evento: str, datos: EventoCreate, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id_evento == id_evento).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    evento.nomEve         = datos.nomEve
    evento.fecha_ini      = datos.fecha_ini
    evento.fecha_fin      = datos.fecha_fin
    evento.descripcion    = datos.descripcion
    evento.id_deporte     = datos.id_deporte
    evento.id_instalacion = datos.id_instalacion
    evento.id_usuario     = datos.id_usuario
    db.commit()
    db.refresh(evento)
    return evento

@router.delete("/{id_evento}")
def eliminar_evento(id_evento: str, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id_evento == id_evento).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    db.delete(evento)
    db.commit()
    return {"mensaje": f"Evento {id_evento} eliminado correctamente"}