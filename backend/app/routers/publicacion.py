from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Publicacion
from app.schemas.schemas import PublicacionCreate, PublicacionRead
import uuid

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"])

@router.get("/", response_model=list[PublicacionRead])
def listar_publicaciones(db: Session = Depends(get_db)):
    return db.query(Publicacion).all()

@router.get("/{id_publi}", response_model=PublicacionRead)
def obtener_publicacion(id_publi: str, db: Session = Depends(get_db)):
    pub = db.query(Publicacion).filter(Publicacion.id_publi == id_publi).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return pub

@router.post("/", response_model=PublicacionRead)
def crear_publicacion(datos: PublicacionCreate, db: Session = Depends(get_db)):
    nueva = Publicacion(
        id_publi    = str(uuid.uuid4())[:20],
        tipo        = datos.tipo,
        titulo      = datos.titulo,
        ruta_img    = datos.ruta_img,
        contenido   = datos.contenido,
        fecha_publi = datos.fecha_publi,
        id_usuario  = datos.id_usuario,
        id_equipo   = datos.id_equipo
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{id_publi}", response_model=PublicacionRead)
def actualizar_publicacion(id_publi: str, datos: PublicacionCreate, db: Session = Depends(get_db)):
    pub = db.query(Publicacion).filter(Publicacion.id_publi == id_publi).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    pub.tipo        = datos.tipo
    pub.titulo      = datos.titulo
    pub.ruta_img    = datos.ruta_img
    pub.contenido   = datos.contenido
    pub.fecha_publi = datos.fecha_publi
    pub.id_usuario  = datos.id_usuario
    pub.id_equipo   = datos.id_equipo
    db.commit()
    db.refresh(pub)
    return pub

@router.delete("/{id_publi}")
def eliminar_publicacion(id_publi: str, db: Session = Depends(get_db)):
    pub = db.query(Publicacion).filter(Publicacion.id_publi == id_publi).first()
    if not pub:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    db.delete(pub)
    db.commit()
    return {"mensaje": f"Publicación {id_publi} eliminada correctamente"}
