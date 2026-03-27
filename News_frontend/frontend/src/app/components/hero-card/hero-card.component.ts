import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';

@Component({
  selector: 'app-hero-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="story" class="hero-content">
      <h1 class="font-headline text-5xl md:text-7xl font-extrabold italic text-on-surface leading-tight tracking-tighter mb-4 uppercase">
        {{ story?.title || 'Initializing AI Core...' }}
      </h1>
      <p class="font-body text-xl text-primary-container/80 leading-relaxed max-w-3xl mb-8">
        {{ story?.summary || 'Standardizing news clusters on TPU hardware...' }}
      </p>
    </div>

    <div *ngIf="!story && loading" class="hero-loading space-y-4">
       <div class="h-16 w-3/4 bg-on-surface/5 animate-pulse rounded-sm"></div>
       <div class="h-16 w-1/2 bg-on-surface/5 animate-pulse rounded-sm"></div>
       <div class="h-6 w-full bg-primary-container/5 animate-pulse rounded-sm mt-8"></div>
    </div>
  `,
  styles: [`
    :host { display: block; }
    .hero-content h1 { text-wrap: balance; }
  `]
})
export class HeroCardComponent implements OnInit {
  story: any;
  loading = true;

  constructor(private news: NewsService) {}

  ngOnInit() {
    this.news.getStoryOfDay().subscribe({
      next: (data: any) => {
        this.story = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load story of the day', err);
        this.loading = false;
      }
    });
  }
}