from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time


# ── Usuario ──────────────────────────────────────────
class UsuarioBase(BaseModel):
    correo: str
    edad: int
    sexo: str
    municipio: str
    nomUsu: str
    telefono: Optional[str] = None
    fecha_creacion: date

class UsuarioCreate(UsuarioBase):
    contrasenha: str

class UsuarioRead(UsuarioBase):
    id_usuario: str
    class Config:
        from_attributes = True


# ── Deporte ───────────────────────────────────────────
class DeporteBase(BaseModel):
    nomDepo: str

class DeporteCreate(DeporteBase):
    id_deporte: str

class DeporteRead(DeporteBase):
    id_deporte: str
    class Config:
        from_attributes = True


# ── Zona ──────────────────────────────────────────────
class ZonaBase(BaseModel):
    nomZona: str
    municipio: str

class ZonaCreate(ZonaBase):
    id_zona: str

class ZonaRead(ZonaBase):
    id_zona: str
    class Config:
        from_attributes = True


# ── Instalacion ───────────────────────────────────────
class InstalacionBase(BaseModel):
    nomInst: str
    id_zona: str

class InstalacionCreate(InstalacionBase):
    id_instalacion: str

class InstalacionRead(InstalacionBase):
    id_instalacion: str
    class Config:
        from_attributes = True


# ── Entrenador ────────────────────────────────────────
class EntrenadorBase(BaseModel):
    anhos_exp: Optional[int] = None
    id_instalacion: str

class EntrenadorCreate(EntrenadorBase):
    id_entrenador: str

class EntrenadorRead(EntrenadorBase):
    id_entrenador: str
    class Config:
        from_attributes = True


# ── Horario ───────────────────────────────────────────
class HorarioBase(BaseModel):
    dias: date
    hora_ini: time
    hora_fin: time
    id_instalacion: str

class HorarioCreate(HorarioBase):
    id_horario: str

class HorarioRead(HorarioBase):
    id_horario: str
    class Config:
        from_attributes = True


# ── Equipo ────────────────────────────────────────────
class EquipoBase(BaseModel):
    nomEqui: str
    cant_int: int
    cat_gen: str
    cat_edad: int
    id_deporte: str

class EquipoCreate(EquipoBase):
    id_equipo: str

class EquipoRead(EquipoBase):
    id_equipo: str
    class Config:
        from_attributes = True


# ── Publicacion ───────────────────────────────────────
class PublicacionBase(BaseModel):
    tipo: str
    titulo: str
    ruta_img: Optional[str] = None
    contenido: Optional[str] = None
    fecha_publi: datetime
    id_usuario: Optional[str] = None
    id_equipo: Optional[str] = None

class PublicacionCreate(PublicacionBase):
    id_publi: str

class PublicacionRead(PublicacionBase):
    id_publi: str
    class Config:
        from_attributes = True


# ── Evento ────────────────────────────────────────────
class EventoBase(BaseModel):
    nomEve: str
    fecha_ini: date
    fecha_fin: date
    descripcion: str
    id_deporte: str
    id_instalacion: str
    id_usuario: str

class EventoCreate(EventoBase):
    id_evento: str

class EventoRead(EventoBase):
    id_evento: str
    class Config:
        from_attributes = True


# ── Reserva ───────────────────────────────────────────
class ReservaBase(BaseModel):
    fecha_resIni: datetime
    fecha_resFin: datetime
    id_usuario: Optional[str] = None
    id_equipo: Optional[str] = None
    id_instalacion: str
    id_horario: str

class ReservaCreate(ReservaBase):
    id_reserva: str

class ReservaRead(ReservaBase):
    id_reserva: str
    class Config:
        from_attributes = True


# ── Inscripcion ───────────────────────────────────────
class InscripcionBase(BaseModel):
    id_equipo: str
    id_evento: str

class InscripcionCreate(InscripcionBase):
    id_inscripcion: str

class InscripcionRead(InscripcionBase):
    id_inscripcion: str
    class Config:
        from_attributes = True