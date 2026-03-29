import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { NewsService } from '../../services/news.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="flex items-center justify-center h-screen bg-background text-on-surface font-body p-6">
      <div class="max-w-md w-full glass-card p-10 space-y-8 border border-primary/20">
        <div class="text-center">
          <h1 class="font-headline text-4xl italic font-bold text-primary">Aureum Terminal</h1>
          <p class="text-xs uppercase tracking-widest text-primary/40 mt-2">Intelligence Authentication</p>
        </div>

        <form (ngSubmit)="login()" class="space-y-6">
          <div class="space-y-2">
            <label class="font-mono text-[0.6rem] uppercase text-primary/60">Node Identity (Username)</label>
            <input [(ngModel)]="username" name="username" type="text" 
                   class="w-full bg-surface-container-low border border-outline-variant p-3 focus:outline-primary transition-all">
          </div>

          <div class="space-y-2">
            <label class="font-mono text-[0.6rem] uppercase text-primary/60">Access Key (Password)</label>
            <input [(ngModel)]="password" name="password" type="password" 
                   class="w-full bg-surface-container-low border border-outline-variant p-3 focus:outline-primary transition-all">
          </div>

          <button type="submit" 
                  class="w-full py-4 bg-primary text-on-primary font-bold uppercase tracking-[0.2em] text-sm hover:brightness-110 shadow-lg">
            Initialize Access
          </button>
        </form>

        <div class="text-center pt-4">
           <a routerLink="/register" class="text-[0.6rem] font-mono text-primary hover:underline uppercase tracking-widest">Construct New Identity (Register)</a>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  http = inject(HttpClient);
  news = inject(NewsService);
  router = inject(Router);
  username = '';
  password = '';

  login() {
    this.http.post(`${this.news.api}/login`, {
       username: this.username,
       password: this.password
    }, { headers: this.news.headers }).subscribe((res: any) => {
      if (res.status === 'success') {
         localStorage.setItem('user', JSON.stringify(res));
         this.router.navigate(['/dashboard']);
      } else {
         alert('Authentication Invalid.');
      }
    });
  }
}
