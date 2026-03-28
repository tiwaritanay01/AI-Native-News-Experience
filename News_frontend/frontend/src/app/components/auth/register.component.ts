import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="flex items-center justify-center min-h-screen bg-background text-on-surface font-body p-6">
      <div class="max-w-2xl w-full glass-card p-12 space-y-12 border border-primary/20">
        <div class="text-center">
          <h1 class="font-headline text-5xl italic font-bold text-primary">Persona Induction</h1>
          <p class="text-xs uppercase tracking-widest text-primary/40 mt-2 italic shadow-sm">Define your intelligence profile</p>
        </div>

        <form (ngSubmit)="register()" class="grid grid-cols-1 md:grid-cols-2 gap-12">
          
          <div class="space-y-6">
            <div class="space-y-2">
              <label class="font-mono text-[0.6rem] uppercase text-primary/60">Choose Node Identity (Username)</label>
              <input [(ngModel)]="username" name="username" type="text" placeholder="Identity_01"
                     class="w-full bg-surface-container-low border border-outline-variant p-4 focus:outline-primary placeholder:opacity-20 font-mono">
            </div>

            <div class="space-y-2">
              <label class="font-mono text-[0.6rem] uppercase text-primary/60">Generate Access Key (Password)</label>
              <input [(ngModel)]="password" name="password" type="password" 
                     class="w-full bg-surface-container-low border border-outline-variant p-4 focus:outline-primary">
            </div>

            <div class="pt-6">
              <button type="submit" 
                      class="w-full py-4 bg-primary text-on-primary font-bold uppercase tracking-[0.2em] text-sm hover:brightness-110 shadow-lg transition-all active:scale-95">
                Construct Persona
              </button>
              <div class="text-center mt-6">
                <a routerLink="/login" class="text-[0.6rem] font-mono text-primary/40 hover:underline uppercase tracking-widest">Existing Profile Detected? (Login)</a>
              </div>
            </div>
          </div>

          <!-- Persona Preference -->
          <div class="space-y-6 border-l border-primary/10 pl-12 text-left">
            <h3 class="font-headline text-xl text-primary font-bold italic mb-6 border-b border-outline-variant/30 pb-4">Personalization Stream</h3>
            
            <div *ngFor="let p of personas" 
                 (click)="persona = p.id"
                 class="group relative p-6 bg-surface-container-low border hover:border-primary/40 cursor-pointer transition-all duration-300"
                 [class.border-primary]="persona === p.id"
                 [class.bg-primary/5]="persona === p.id">
              <div class="flex justify-between items-start">
                <h4 class="font-bold text-sm text-primary uppercase tracking-widest">{{ p.id }}</h4>
                <div *ngIf="persona === p.id" class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></div>
              </div>
              <p class="text-[0.65rem] text-on-surface/50 mt-1 first-letter:text-lg first-letter:font-headline">{{ p.desc }}</p>
              
              <div *ngIf="persona === p.id" class="absolute -left-1.5 top-0 bottom-0 w-1 bg-primary"></div>
            </div>
          </div>
        </form>
      </div>
    </div>
  `
})
export class RegisterComponent {
  http = inject(HttpClient);
  router = inject(Router);
  username = '';
  password = '';
  persona = 'Investor';

  personas = [
    { id: 'Investor', desc: 'Focus on portfolio health, volatility signals, and risk assessment metrics.' },
    { id: 'Founder', desc: 'Strategic intelligence on funding, competitor moves, and disruptive technologies.' },
    { id: 'Student', desc: 'Educational lens: explaining complex jargon using analogies and "Why it Matters" logic.' }
  ];

  register() {
    this.http.post('http://localhost:8000/register', {
       username: this.username,
       password: this.password,
       persona: this.persona
    }).subscribe((res: any) => {
      if (res.status === 'success') {
         this.router.navigate(['/login']);
      } else {
         alert('Registration Interrupted. Node already exists.');
      }
    });
  }
}
