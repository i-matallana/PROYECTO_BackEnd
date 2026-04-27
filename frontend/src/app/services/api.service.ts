import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Evento {
  id: number;
  nombre: string;
  descripcion: string;
  imagen: string;
  tags?: string[];
  meta?: string[];
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  // URL base de la API de backend en FastAPI
  private readonly baseUrl = 'http://localhost:8000';

  constructor(private readonly http: HttpClient) {}

  // Llama al endpoint /evento de la API para obtener la lista de eventos
  getEventos(): Observable<Evento[]> {
    return this.http.get<Evento[]>(`${this.baseUrl}/evento`);
  }
}
