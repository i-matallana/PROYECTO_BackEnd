
from sqlalchemy import (
    Column, String, Integer, Date, DateTime,
    Time, Text, ForeignKey, CHAR
)
from app.config.db import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario     = Column(String(36), primary_key=True)
    correo         = Column(String(50), nullable=False)
    edad           = Column(Integer, nullable=False)
    sexo           = Column(CHAR(1), nullable=False)
    municipio      = Column(String(20), nullable=False)
    contrasenha    = Column(String(20), nullable=False)
    nomUsu         = Column(String(50), nullable=False)
    telefono       = Column(String(11))
    fecha_creacion = Column(Date, nullable=False)


class Deporte(Base):
    __tablename__ = "deporte"

    id_deporte = Column(String(50), primary_key=True)
    nomDepo    = Column(String(20), nullable=False)


class Zona(Base):
    __tablename__ = "zona"

    id_zona   = Column(String(20), primary_key=True)
    nomZona   = Column(String(20), nullable=False)
    municipio = Column(String(20), nullable=False)


class Instalacion(Base):
    __tablename__ = "instalacion"

    id_instalacion = Column(String(20), primary_key=True)
    nomInst        = Column(String(50), nullable=False)
    id_zona        = Column(String(20), ForeignKey("zona.id_zona"), nullable=False)


class Entrenador(Base):
    __tablename__ = "entrenador"

    id_entrenador  = Column(String(20), primary_key=True)
    anhos_exp      = Column(Integer)
    id_instalacion = Column(String(20), ForeignKey("instalacion.id_instalacion"), nullable=False)


class Horario(Base):
    __tablename__ = "horarios"

    id_horario     = Column(String(20), primary_key=True)
    dias           = Column(Date, nullable=False)
    hora_ini       = Column(Time, nullable=False)
    hora_fin       = Column(Time, nullable=False)
    id_instalacion = Column(String(20), ForeignKey("instalacion.id_instalacion"), nullable=False)


class Equipo(Base):
    __tablename__ = "equipo"

    id_equipo  = Column(String(20), primary_key=True)
    nomEqui    = Column(String(50), nullable=False)
    cant_int   = Column(Integer, nullable=False)
    cat_gen    = Column(CHAR(1), nullable=False)
    cat_edad   = Column(Integer, nullable=False)
    id_deporte = Column(String(50), ForeignKey("deporte.id_deporte"), nullable=False)


class Publicacion(Base):
    __tablename__ = "publicacion"

    id_publi    = Column(String(20), primary_key=True)
    tipo        = Column(String(10), nullable=False)
    titulo      = Column(Text, nullable=False)
    ruta_img    = Column(String(100))
    contenido   = Column(Text)
    fecha_publi = Column(DateTime, nullable=False)
    id_usuario  = Column(String(50), ForeignKey("usuario.id_usuario"))
    id_equipo   = Column(String(20), ForeignKey("equipo.id_equipo"))


class Evento(Base):
    __tablename__ = "evento"

    id_evento      = Column(String(20), primary_key=True)
    nomEve         = Column(String(20), nullable=False)
    fecha_ini      = Column(Date, nullable=False)
    fecha_fin      = Column(Date, nullable=False)
    descripcion    = Column(Text, nullable=False)
    id_deporte     = Column(String(50), ForeignKey("deporte.id_deporte"), nullable=False)
    id_instalacion = Column(String(20), ForeignKey("instalacion.id_instalacion"), nullable=False)
    id_usuario     = Column(String(50), ForeignKey("usuario.id_usuario"), nullable=False)


class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva     = Column(String(20), primary_key=True)
    fecha_resIni   = Column(DateTime, nullable=False)
    fecha_resFin   = Column(DateTime, nullable=False)
    id_usuario     = Column(String(50), ForeignKey("usuario.id_usuario"))
    id_equipo      = Column(String(20), ForeignKey("equipo.id_equipo"))
    id_instalacion = Column(String(20), ForeignKey("instalacion.id_instalacion"), nullable=False)
    id_horario     = Column(String(20), ForeignKey("horarios.id_horario"), nullable=False)


class Inscripcion(Base):
    __tablename__ = "inscripcion"

    id_inscripcion = Column(String(20), primary_key=True)
    id_equipo      = Column(String(20), ForeignKey("equipo.id_equipo"), nullable=False)
    id_evento      = Column(String(20), ForeignKey("evento.id_evento"), nullable=False)


class IntegranteEquipo(Base):
    __tablename__ = "integrante_equipo"

    rol_equipo = Column(String(30), nullable=False, primary_key=True)
    id_usuario = Column(String(50), ForeignKey("usuario.id_usuario"), primary_key=True)
    id_equipo  = Column(String(20), ForeignKey("equipo.id_equipo"), primary_key=True)


class UsuarioDeporte(Base):
    __tablename__ = "usuario_deporte"

    id_usuario = Column(String(50), ForeignKey("usuario.id_usuario"), primary_key=True)
    id_deporte = Column(String(50), ForeignKey("deporte.id_deporte"), primary_key=True)


class EntrenadorDeporte(Base):
    __tablename__ = "entrenador_deporte"

    id_entrenador = Column(String(20), ForeignKey("entrenador.id_entrenador"), primary_key=True)
    id_deporte    = Column(String(50), ForeignKey("deporte.id_deporte"), primary_key=True)


class DeporteInstalacion(Base):
    __tablename__ = "deporte_instalacion"

    id_deporte     = Column(String(50), ForeignKey("deporte.id_deporte"), primary_key=True)
    id_instalacion = Column(String(20), ForeignKey("instalacion.id_instalacion"), primary_key=True)