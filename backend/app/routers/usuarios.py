from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioRead
import uuid
from datetime import date

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# GET todos 
@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


# GET ID 
@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# crear
@router.post("/", response_model=UsuarioRead)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar que el correo no esté repetido
    existe = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo = Usuario(
        id_usuario     = str(uuid.uuid4()),
        correo         = datos.correo,
        edad           = datos.edad,
        sexo           = datos.sexo,
        municipio      = datos.municipio,
        contrasenha    = datos.contrasenha,
        nomUsu         = datos.nomUsu,
        telefono       = datos.telefono,
        fecha_creacion = date.today()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# actualizar 
@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(id_usuario: str, datos: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.correo      = datos.correo
    usuario.edad        = datos.edad
    usuario.sexo        = datos.sexo
    usuario.municipio   = datos.municipio
    usuario.contrasenha = datos.contrasenha
    usuario.nomUsu      = datos.nomUsu
    usuario.telefono    = datos.telefono

    db.commit()
    db.refresh(usuario)
    return usuario


# eliminar
@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario {id_usuario} eliminado correctamente"}