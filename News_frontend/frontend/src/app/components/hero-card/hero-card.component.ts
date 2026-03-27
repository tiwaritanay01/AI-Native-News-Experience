import { Component, OnInit, Input, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';

@Component({
  selector: 'app-hero-card',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
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
  @Input() story: any;
  @Input() loading = false;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    // Manually trigger detection if story is passed in late
    this.cdr.detectChanges();
  }
}