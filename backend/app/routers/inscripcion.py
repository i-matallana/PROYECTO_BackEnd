from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Inscripcion
from app.schemas.schemas import InscripcionCreate, InscripcionRead
import uuid

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])

@router.get("/", response_model=list[InscripcionRead])
def listar_inscripciones(db: Session = Depends(get_db)):
    return db.query(Inscripcion).all()

@router.get("/{id_inscripcion}", response_model=InscripcionRead)
def obtener_inscripcion(id_inscripcion: str, db: Session = Depends(get_db)):
    insc = db.query(Inscripcion).filter(Inscripcion.id_inscripcion == id_inscripcion).first()
    if not insc:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return insc

@router.post("/", response_model=InscripcionRead)
def crear_inscripcion(datos: InscripcionCreate, db: Session = Depends(get_db)):
    nueva = Inscripcion(
        id_inscripcion = str(uuid.uuid4())[:20],
        id_equipo      = datos.id_equipo,
        id_evento      = datos.id_evento
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.delete("/{id_inscripcion}")
def eliminar_inscripcion(id_inscripcion: str, db: Session = Depends(get_db)):
    insc = db.query(Inscripcion).filter(Inscripcion.id_inscripcion == id_inscripcion).first()
    if not insc:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    db.delete(insc)
    db.commit()
    return {"mensaje": f"Inscripción {id_inscripcion} eliminada correctamente"}
