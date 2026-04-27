import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    // Escucha errores globales del navegador
    provideBrowserGlobalErrorListeners(),
    // Router de Angular, aunque ahora no usamos rutas específicas
    provideRouter(routes),
    // Habilita HttpClient para hacer peticiones al backend
    provideHttpClient(),
    // Proporciona hidratación para SSR si se usa en el proyecto
    provideClientHydration(withEventReplay())
  ]
};
