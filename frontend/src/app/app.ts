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

  // Eventos
  eventosCercanos = signal<Evento[]>([]);
  eventosProximos = signal<Evento[]>([]);

  // Buscador y filtros
  buscadorTexto = '';  // plain string for ngModel
  filtrosAbiertos = signal(false);
  filtrosSeleccionados = signal<string[]>([]);

  // Perfil
  activeTab = signal('Reservas');

  // Estadísticas animadas
  statEventos = signal(0);
  statEspacios = signal(0);
  statMunicipios = signal(0);

  // Imágenes de deportes para tarjetas de eventos
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
      this.cargarEventos();
      this.animarStats();
    }
  }

  ngOnDestroy() {
    if (this.carouselInterval) clearInterval(this.carouselInterval);
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

  // Modales login / signup
  toggleLogin() {
    this.showLogin.set(!this.showLogin());
    if (this.showSignup()) this.showSignup.set(false);
  }

  toggleSignup() {
    this.showSignup.set(!this.showSignup());
    if (this.showLogin()) this.showLogin.set(false);
  }

  // Cargar eventos desde API con fallback de ejemplo
  private cargarEventos() {
    this.apiService.getEventos().subscribe({
      next: (data: Evento[]) => {
        const hoy = new Date(); hoy.setHours(0, 0, 0, 0);
        setTimeout(() => {
          this.eventosCercanos.set(data.filter(ev => ev.municipio === 'Cartagena'));
          this.eventosProximos.set(
            data.filter(ev => new Date(ev.fecha) >= hoy)
                .sort((a, b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime())
          );
          this.cdr.detectChanges();
        });
      },
      error: () => {
        setTimeout(() => {
          this.eventosCercanos.set([
            { id: 1, nombre: 'Torneo Barrial', descripcion: 'Liga local de fútbol con partidos en el estadio municipal.', deporte: 'Fútbol', fecha: '2026-05-10', hora: '16:00', municipio: 'Cartagena' },
            { id: 2, nombre: 'Nado Libre', descripcion: 'Competencia de natación en piscina olímpica para todas las edades.', deporte: 'Natación', fecha: '2026-05-15', hora: '10:00', municipio: 'Cartagena' },
            { id: 3, nombre: 'Basket 3x3', descripcion: 'Torneo callejero de baloncesto en la plaza central.', deporte: 'Baloncesto', fecha: '2026-05-18', hora: '09:00', municipio: 'Cartagena' },
            { id: 4, nombre: 'Ciclismo Urbano', descripcion: 'Recorrido ciclístico por las rutas del barrio histórico.', deporte: 'Ciclismo', fecha: '2026-05-20', hora: '07:00', municipio: 'Cartagena' },
          ]);
          this.eventosProximos.set([
            { id: 5, nombre: 'Maratón Bolívar', descripcion: 'Carrera atlética de 10km por el centro histórico de Cartagena.', deporte: 'Running', fecha: '2026-06-01', hora: '06:00', municipio: 'Cartagena' },
            { id: 6, nombre: 'Torneo de Voleibol', descripcion: 'Campeonato municipal de voleibol playa en las canchas del litoral.', deporte: 'Voleibol', fecha: '2026-06-05', hora: '08:00', municipio: 'Turbaco' },
            { id: 7, nombre: 'Boxeo Aficionado', descripcion: 'Velada de boxeo aficionado con categorías juvenil y senior.', deporte: 'Boxeo', fecha: '2026-06-10', hora: '18:00', municipio: 'Arjona' },
          ]);
          this.cdr.detectChanges();
        });
      }
    });
  }

  // Modal de evento
  abrirModal(evento: Evento) {
    this.selectedEvento.set(evento);
    this.showModal.set(true);
  }

  cerrarModal() {
    this.showModal.set(false);
    this.selectedEvento.set(null);
  }

  cerrarOverlay() { this.cerrarModal(); }

  // Filtros de espacios
  toggleFiltros() { this.filtrosAbiertos.set(!this.filtrosAbiertos()); }
  abrirFiltros()  { this.filtrosAbiertos.set(true); }

  actualizarTags(event: any) {
    const cb = event.target as HTMLInputElement;
    const tag = cb.dataset['tag'] || '';
    if (cb.checked) {
      if (!this.filtrosSeleccionados().includes(tag))
        this.filtrosSeleccionados.set([...this.filtrosSeleccionados(), tag]);
    } else {
      this.filtrosSeleccionados.set(this.filtrosSeleccionados().filter(t => t !== tag));
    }
  }

  quitarTag(tag: string) {
    this.filtrosSeleccionados.set(this.filtrosSeleccionados().filter(t => t !== tag));
  }

  limpiar() { this.filtrosSeleccionados.set([]); }
  buscar()  { this.filtrosAbiertos.set(false); }

  // Perfil
  activeTab$ = signal('Reservas');
  changeTab(tab: string) { this.activeTab.set(tab); }

  perfilUsuario = signal({
    username: 'nombre_usuario',
    edad: 25,
    municipio: 'Cartagena',
    genero: '♂',
    instagram_url: '',
    tiktok_url: '',
    nombre_equipo: ''
  });

  // Formularios
  crearCuenta(event: Event) { event.preventDefault(); console.log('Crear cuenta'); }
  iniciarSesion(event: Event) { event.preventDefault(); console.log('Iniciar sesión'); }

  // Scroll del carrusel de eventos
  scrollCarrusel(elementId: string, direction: number) {
    const el = document.getElementById(elementId);
    if (el) el.scrollBy({ left: direction * 320, behavior: 'smooth' });
  }

  // Filtros
  zonas = [
    { id: 1, nombre: 'Norte - Centro y Getsemaní', tag: 'ZNTE01' },
    { id: 2, nombre: 'Norte - Residencial', tag: 'ZNTE02' },
    { id: 3, nombre: 'Nueva Zona Norte', tag: 'ZNTE03' },
    { id: 4, nombre: 'Península Turística', tag: 'ZCTO01' },
    { id: 5, nombre: 'Residencial Central-Sur', tag: 'ZCTO02' },
    { id: 6, nombre: 'Suroriente y Suroccidente', tag: 'ZSUR01' },
    { id: 7, nombre: 'Extremo Sur (Industrial)', tag: 'ZSUR02' }
  ];

  municipios = [
    { id: 1, nombre: 'Cartagena' }, { id: 2, nombre: 'Carmen de Bolívar' },
    { id: 3, nombre: 'San Juan Nepomuceno' }, { id: 4, nombre: 'Arjona' },
    { id: 5, nombre: 'Turbaco' }, { id: 6, nombre: 'Mompox' }, { id: 7, nombre: 'Magangué' }
  ];

  deportes = [
    { id: 1, nombre: 'Fútbol' }, { id: 2, nombre: 'Baloncesto' }, { id: 3, nombre: 'Natación' },
    { id: 4, nombre: 'Tenis' }, { id: 5, nombre: 'Boxeo' }, { id: 6, nombre: 'Halterofilia' },
    { id: 7, nombre: 'Atletismo' }, { id: 8, nombre: 'Calistenia' }, { id: 9, nombre: 'Ciclismo' },
    { id: 10, nombre: 'Softbol' }, { id: 11, nombre: 'Voleibol' }
  ];

  tiposInstalacion = [
    { id: 1, nombre: 'Público' }, { id: 2, nombre: 'Privado' }
  ];

  // Getter eventos filtrados
  get eventosCercanosFiltrados() {
    const eventos = this.eventosCercanos();
    const filtros = this.filtrosSeleccionados();
    if (!filtros.length) return eventos;
    return eventos.filter(ev =>
      filtros.some(f => ev.deporte === f || ev.municipio === f)
    );
  }

  // Animación JS de contadores de estadísticas
  private animarStats() {
    const targets = { eventos: 24, espacios: 57, municipios: 45 };
    const steps = 60;
    const duration = 2500;
    let step = 0;
    const interval = setInterval(() => {
      step++;
      const p = step / steps;
      this.statEventos.set(Math.round(targets.eventos * p));
      this.statEspacios.set(Math.round(targets.espacios * p));
      this.statMunicipios.set(Math.round(targets.municipios * p));
      if (step >= steps) clearInterval(interval);
    }, duration / steps);
  }
}
