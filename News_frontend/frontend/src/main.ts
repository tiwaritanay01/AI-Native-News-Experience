
import { appConfig } from './app/app.config';
import { App } from './app/app';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideClientHydration } from '@angular/platform-browser';



bootstrapApplication(App, {
  ...appConfig,
  providers: [
    ...(appConfig.providers ?? []),
    provideClientHydration()
  ]
});

