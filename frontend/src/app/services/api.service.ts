import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface Evento {
  id: string | number;
  nombre: string;
  descripcion: string;
  deporte: string;
  fecha: string;
  hora: string;
  municipio: string;
  emoji?: string;
  bg?: string;
  tags?: string[];
  meta?: string[];
}

interface EventoApi {
  id_evento?: string;
  nomEve: string;
  fecha_ini: string;
  fecha_fin?: string;
  descripcion: string;
  id_deporte: string;
  id_instalacion?: string;
  id_usuario?: string;
  emoji?: string;
  bg?: string;
  tags?: string[];
  meta?: string[];
  [prop: string]: any;
}

export interface ApiResource {
  [key: string]: any;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  // URL base de la API del backend Python/FastAPI
  private readonly baseUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient) {}

  private get<T>(path: string): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}/${path}`);
  }

  private post<T>(path: string, body: unknown): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}/${path}`, body);
  }

  private put<T>(path: string, body: unknown): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}/${path}`, body);
  }

  private patch<T>(path: string, body: unknown): Observable<T> {
    return this.http.patch<T>(`${this.baseUrl}/${path}`, body);
  }

  private delete<T>(path: string): Observable<T> {
    return this.http.delete<T>(`${this.baseUrl}/${path}`);
  }

  getEventos(): Observable<Evento[]> {
    return this.get<EventoApi[]>('eventos').pipe(
      map((data) => data.map((evento) => this.normalizeEvento(evento)))
    );
  }

  getEventoById(id: string): Observable<EventoApi> {
    return this.get<EventoApi>(`eventos/${id}`);
  }

  getDeportes(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('deportes');
  }

  getEntrenadores(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('entrenadores');
  }

  getEquipos(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('equipos');
  }

  getHorarios(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('horarios');
  }

  getInstalaciones(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('instalaciones');
  }

  getZonas(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('zonas');
  }

  getReservas(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('reservas');
  }

  getPublicaciones(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('publicaciones');
  }

  getInscripciones(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('inscripciones');
  }

  getUsuarios(): Observable<ApiResource[]> {
    return this.get<ApiResource[]>('usuarios');
  }

  createResource<T>(resource: string, body: unknown): Observable<T> {
    return this.post<T>(resource, body);
  }

  updateResource<T>(resource: string, body: unknown): Observable<T> {
    return this.put<T>(resource, body);
  }

  patchResource<T>(resource: string, body: unknown): Observable<T> {
    return this.patch<T>(resource, body);
  }

  deleteResource<T>(resource: string): Observable<T> {
    return this.delete<T>(resource);
  }

  private normalizeEvento(eventoApi: EventoApi): Evento {
    return {
      id: eventoApi.id_evento || '0',
      nombre: eventoApi.nomEve,
      descripcion: eventoApi.descripcion,
      deporte: eventoApi.id_deporte || 'Desconocido',
      fecha: eventoApi.fecha_ini,
      hora: eventoApi.fecha_fin || '',
      municipio: 'Cartagena',
      emoji: eventoApi.emoji || '⚽',
      bg: eventoApi.bg || '#e8f5e9',
      tags: eventoApi.tags || [eventoApi.id_deporte || 'Evento'],
      meta: eventoApi.meta || []
    };
  }
}
