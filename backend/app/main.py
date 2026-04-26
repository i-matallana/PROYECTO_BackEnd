from fastapi import FastAPI
from app.routers import (
    usuarios, deporte, zona, instalacion,
    entrenador, horario, equipo, publicacion,
    evento, reserva, inscripcion
)

app = FastAPI(title="SportPoint API", version="1.0.0")

app.include_router(usuarios.router)
app.include_router(deporte.router)
app.include_router(zona.router)
app.include_router(instalacion.router)
app.include_router(entrenador.router)
app.include_router(horario.router)
app.include_router(equipo.router)
app.include_router(publicacion.router)
app.include_router(evento.router)
app.include_router(reserva.router)
app.include_router(inscripcion.router)