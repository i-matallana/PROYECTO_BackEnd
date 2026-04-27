import { Component, signal, OnInit, OnDestroy, inject, Inject, PLATFORM_ID, ChangeDetectorRef, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { isPlatformBrowser } from '@angular/common';
import { ApiService, Evento } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.scss'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class App implements OnInit, OnDestroy {
  private apiService = inject(ApiService);
  private cdr = inject(ChangeDetectorRef);

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  // Estado reactivo de navegación
  activeSection = signal('Inicio');
  showLogin = signal(false);
  showSignup = signal(false);
  showModal = signal(false);
  selectedEvento = signal<Evento | null>(null);

  // Carrusel de imágenes hero
  slides = signal([
    'assets/photos/paralimpicos_yamil.jpg',
    'assets/photos/niños_aerobicos.jpg',
    'assets/photos/patinadores_montemaria.jpg'
  ]);
  currentSlide = signal(0);
  private carouselInterval: any;

  // Eventos e Instalaciones
  eventosCercanos = signal<Evento[]>([]);
  eventosProximos = signal<Evento[]>([]);
  instalaciones = signal<any[]>([]);

  // Buscador y filtros
  buscadorTexto = '';
  filtrosAbiertos = signal(false);
  filtrosSeleccionados = signal<string[]>([]);

  // Perfil
  activeTab = signal('Reservas');
  perfilUsuario = signal({
    username: 'cargando...',
    edad: 0,
    municipio: '...',
    genero: '...',
    instagram_url: '',
    tiktok_url: '',
    nombre_equipo: ''
  });

  // Estadísticas animadas
  statEventos = signal(0);
  statEspacios = signal(0);
  statMunicipios = signal(0);

  // Imágenes de deportes
  imagenesDeporte: { [key: string]: string } = {
    'Fútbol':      'assets/img/futbolevento.png',
    'Baloncesto':  'assets/img/baloncestoevento.png',
    'Natación':    'assets/img/natacionevento.png',
    'Tenis':       'assets/img/tenisevento.png',
    'Boxeo':       'assets/img/boxeoevento.png',
    'Halterofilia':'assets/img/halterofiliaevento.png',
    'Running':     'assets/img/runningevento.png',
    'Calistenia':  'assets/img/calisteniaevento.png',
    'Ciclismo':    'assets/img/ciclismoevento.png',
    'Softbol':     'assets/img/softbolevento.png',
    'Voleibol':    'assets/img/voleibolevento.png',
  };

  ngOnInit() {
    this.iniciarCarrusel();
    if (isPlatformBrowser(this.platformId)) {
      this.cargarTodo();
      this.animarStats();
    }
  }

  ngOnDestroy() {
    if (this.carouselInterval) clearInterval(this.carouselInterval);
  }

  // Carga global de datos
  private cargarTodo() {
    this.cargarEventos();
    this.cargarInstalaciones();
    this.cargarPerfil();
  }

  // Navegación
  changeSection(section: string) {
    this.activeSection.set(section);
  }

  // Carrusel hero
  changeSlide(direction: number) {
    const total = this.slides().length;
    this.currentSlide.set((this.currentSlide() + direction + total) % total);
  }

  goToSlide(index: number) {
    this.currentSlide.set(index);
  }

  private iniciarCarrusel() {
    this.carouselInterval = setInterval(() => this.changeSlide(1), 4000);
  }

  // Modales
  toggleLogin() { this.showLogin.set(!this.showLogin()); if (this.showSignup()) this.showSignup.set(false); }
  toggleSignup() { this.showSignup.set(!this.showSignup()); if (this.showLogin()) this.showLogin.set(false); }

  // Cargar eventos
  private cargarEventos() {
    this.apiService.getEventos().subscribe({
      next: (data: Evento[]) => {
        this.eventosCercanos.set(data.filter(ev => ev.municipio === 'Cartagena'));
        const hoy = new Date(); hoy.setHours(0,0,0,0);
        this.eventosProximos.set(data.filter(ev => new Date(ev.fecha) >= hoy).sort((a,b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime()));
        this.cdr.detectChanges();
      },
      error: () => this.cargarEventosFallback()
    });
  }

  private cargarEventosFallback() {
    const fallbackData: Evento[] = [
      { id: 1, nombre: "Torneo Barrial", descripcion: "Liga local de fútbol en fase eliminatoria.", deporte: "Fútbol", fecha: "2026-05-10", hora: "16:00", municipio: "Cartagena" },
      { id: 2, nombre: "Basketball Cup", descripcion: "Campeonato juvenil categoría 14-18 años.", deporte: "Baloncesto", fecha: "2026-05-12", hora: "18:00", municipio: "Cartagena" },
      { id: 3, nombre: "Nado Libre", descripcion: "Competencia en piscina olímpica.", deporte: "Natación", fecha: "2026-05-15", hora: "10:00", municipio: "Cartagena" },
      { id: 4, nombre: "Torneo Universitario", descripcion: "UTB vs UDC - Gran Final.", deporte: "Softbol", fecha: "2026-04-28", hora: "16:00", municipio: "Cartagena" },
      { id: 5, nombre: "Femenina Bolivarense", descripcion: "Selecciones Sub-20 en competencia.", deporte: "Voleibol", fecha: "2026-05-01", hora: "08:00", municipio: "Cartagena" },
      { id: 6, nombre: "Amateur Peso Pluma", descripcion: "Velada de boxeo aficionado.", deporte: "Boxeo", fecha: "2026-05-04", hora: "18:00", municipio: "Cartagena" },
      { id: 7, nombre: "Carrera 10K", descripcion: "Running urbano por las calles.", deporte: "Running", fecha: "2026-05-20", hora: "06:00", municipio: "Turbaco" },
      { id: 8, nombre: "Copa Tenis", descripcion: "Torneo abierto nivel aficionado.", deporte: "Tenis", fecha: "2026-05-18", hora: "09:00", municipio: "Cartagena" },
      { id: 9, nombre: "Ciclismo Ruta", descripcion: "Competencia regional de ruta.", deporte: "Ciclismo", fecha: "2026-05-25", hora: "07:00", municipio: "Turbaco" },
      { id: 10, nombre: "Calistenia Park", descripcion: "Exhibición urbana y competencia.", deporte: "Calistenia", fecha: "2026-05-22", hora: "17:00", municipio: "Cartagena" },
      { id: 11, nombre: "Halterofilia Open", descripcion: "Competencia de fuerza máxima.", deporte: "Halterofilia", fecha: "2026-05-28", hora: "15:00", municipio: "Cartagena" },
      { id: 12, nombre: "Boxeo Amateur", descripcion: "Velada deportiva comunitaria.", deporte: "Boxeo", fecha: "2026-05-30", hora: "19:00", municipio: "Magangue" }
    ];
    this.eventosCercanos.set(fallbackData.filter(ev => ev.municipio === 'Cartagena'));
    const hoy = new Date(); hoy.setHours(0,0,0,0);
    this.eventosProximos.set(fallbackData.filter(ev => new Date(ev.fecha) >= hoy).sort((a,b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime()));
    this.cdr.detectChanges();
  }

  // Cargar Instalaciones
  private cargarInstalaciones() {
    this.apiService.getInstalaciones().subscribe({
      next: (data) => {
        this.instalaciones.set(data);
        this.cdr.detectChanges();
      },
      error: () => {
        this.instalaciones.set([
          { id_instalacion: 'I1', nomInst: 'Estadio Municipal de Cartagena', id_zona: 'ZNTE01' },
          { id_instalacion: 'I2', nomInst: 'Polideportivo Central', id_zona: 'ZCTO02' },
          { id_instalacion: 'I3', nomInst: 'Complejo Acuático Bolívar', id_zona: 'ZSUR01' }
        ]);
      }
    });
  }

  // Cargar Perfil
  private cargarPerfil() {
    this.apiService.getUsuarios().subscribe({
      next: (users) => {
        if (users && users.length > 0) {
          const user = users[0];
          this.perfilUsuario.set({
            username: user.nomUsu || 'usuario',
            edad: user.edad || 0,
            municipio: user.municipio || 'Cartagena',
            genero: user.sexo === 'femenino' ? '♀' : '♂',
            instagram_url: '',
            tiktok_url: '',
            nombre_equipo: ''
          });
          this.cdr.detectChanges();
        }
      },
      error: () => {
        this.perfilUsuario.set({
          username: 'usuario_demo',
          edad: 22,
          municipio: 'Cartagena',
          genero: '♂',
          instagram_url: '',
          tiktok_url: '',
          nombre_equipo: 'Equipo Bolívar'
        });
      }
    });
  }

  // Resto de métodos (scroll, filtros, etc.)
  abrirModal(evento: Evento) { this.selectedEvento.set(evento); this.showModal.set(true); }
  cerrarModal() { this.showModal.set(false); this.selectedEvento.set(null); }
  scrollCarrusel(elementId: string, direction: number) {
    const el = document.getElementById(elementId);
    if (el) el.scrollBy({ left: direction * 200, behavior: 'smooth' });
  }

  actualizarTags(event: any) {
    const cb = event.target as HTMLInputElement;
    const tag = cb.dataset['tag'] || '';
    if (cb.checked) { if (!this.filtrosSeleccionados().includes(tag)) this.filtrosSeleccionados.set([...this.filtrosSeleccionados(), tag]); }
    else { this.filtrosSeleccionados.set(this.filtrosSeleccionados().filter(t => t !== tag)); }
  }
  quitarTag(tag: string) { this.filtrosSeleccionados.set(this.filtrosSeleccionados().filter(t => t !== tag)); }
  limpiar() { this.filtrosSeleccionados.set([]); }
  buscar() { this.filtrosAbiertos.set(false); }
  changeTab(tab: string) { this.activeTab.set(tab); }

  private animarStats() {
    const targets = { eventos: 24, espacios: 57, municipios: 45 };
    const steps = 60; const duration = 2500; let step = 0;
    const interval = setInterval(() => {
      step++; const p = step / steps;
      this.statEventos.set(Math.round(targets.eventos * p));
      this.statEspacios.set(Math.round(targets.espacios * p));
      this.statMunicipios.set(Math.round(targets.municipios * p));
      if (step >= steps) clearInterval(interval);
    }, duration / steps);
  }

  get eventosCercanosFiltrados() {
    const eventos = this.eventosCercanos();
    const filtros = this.filtrosSeleccionados();
    if (!filtros.length) return eventos;
    return eventos.filter(ev => filtros.some(f => ev.deporte === f || ev.municipio === f));
  }

  zonas = [{ id: 1, nombre: 'Norte - Centro y Getsemaní', tag: 'ZNTE01' }, { id: 2, nombre: 'Norte - Residencial', tag: 'ZNTE02' }, { id: 3, nombre: 'Nueva Zona Norte', tag: 'ZNTE03' }, { id: 4, nombre: 'Península Turística', tag: 'ZCTO01' }, { id: 5, nombre: 'Residencial Central-Sur', tag: 'ZCTO02' }, { id: 6, nombre: 'Suroriente y Suroccidente', tag: 'ZSUR01' }, { id: 7, nombre: 'Extremo Sur (Industrial)', tag: 'ZSUR02' }];
  municipios = [{ id: 1, nombre: 'Cartagena' }, { id: 2, nombre: 'Carmen de Bolívar' }, { id: 3, nombre: 'San Juan Nepomuceno' }, { id: 4, nombre: 'Arjona' }, { id: 5, nombre: 'Turbaco' }, { id: 6, nombre: 'Mompox' }, { id: 7, nombre: 'Magangué' }];
  deportes = [{ id: 1, nombre: 'Fútbol' }, { id: 2, nombre: 'Baloncesto' }, { id: 3, nombre: 'Natación' }, { id: 4, nombre: 'Tenis' }, { id: 5, nombre: 'Boxeo' }, { id: 6, nombre: 'Halterofilia' }, { id: 7, nombre: 'Atletismo' }, { id: 8, nombre: 'Calistenia' }, { id: 9, nombre: 'Ciclismo' }, { id: 10, nombre: 'Softbol' }, { id: 11, nombre: 'Voleibol' }];
  tiposInstalacion = [{ id: 1, nombre: 'Público' }, { id: 2, nombre: 'Privado' }];
}
