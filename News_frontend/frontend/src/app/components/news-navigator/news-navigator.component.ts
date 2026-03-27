import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';
import { Router } from '@angular/router';
import { SidebarNavigationComponent } from '../sidebar-navigation/sidebar-navigation.component';

@Component({
  selector: 'app-news-navigator',
  standalone: true,
  imports: [CommonModule, SidebarNavigationComponent],
  template: `
    <div class="flex h-screen bg-background text-on-background overflow-hidden font-body ml-20">
      <app-sidebar-navigation></app-sidebar-navigation>
      
      <main class="flex-1 overflow-auto p-8 no-scrollbar bg-surface-container-lowest">
        <header class="mb-12">
          <div class="flex items-center gap-4 mb-2">
            <span class="material-symbols-outlined text-primary text-3xl">explore</span>
            <h1 class="font-headline text-5xl italic font-bold text-primary">News Navigator</h1>
          </div>
          <p class="text-primary-container/60 font-mono text-[0.65rem] uppercase tracking-[0.2em]">Active JAX Intelligence Clustering Signal: Stable</p>
        </header>

        <section class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div *ngFor="let story of stories; let i = index" 
               (click)="openStory(story.cluster_id)"
               class="glass-card border border-primary-container/10 p-6 flex flex-col gap-4 cursor-pointer hover:border-primary/40 transition-all hover:-translate-y-1 group">
            
            <div class="flex justify-between items-start">
               <span class="text-[0.625rem] font-mono text-primary-container/40 uppercase tracking-widest italic">Story.Node_{{ story.cluster_id }}</span>
               <div class="w-1.5 h-1.5 rounded-full bg-secondary-container animate-pulse"></div>
            </div>

            <h3 class="font-headline text-xl font-bold leading-tight group-hover:text-primary transition-colors italic">
              {{ story.title }}
            </h3>
            
            <p class="text-xs text-on-surface/70 line-clamp-3 leading-relaxed">
              {{ story.summary }}
            </p>

            <div class="mt-auto pt-4 border-t border-outline-variant/10 flex justify-between items-center opacity-40 group-hover:opacity-100 transition-opacity">
               <span class="text-[0.6rem] font-mono uppercase tracking-tighter">Impact Score: 8.4/10</span>
               <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </div>
          </div>

          <div *ngIf="stories.length === 0" class="col-span-full py-20 flex flex-col items-center justify-center opacity-30 gap-4">
             <div class="w-12 h-1 bg-primary-container animate-pulse"></div>
             <p class="font-mono text-xs uppercase tracking-widest">Awaiting story stream synchronization...</p>
          </div>
        </section>
      </main>
    </div>
  `,
  styles: [`:host { display: block; }`]
})
export class NewsNavigatorComponent implements OnInit {
  news = inject(NewsService);
  router = inject(Router);
  stories: any[] = [];

  ngOnInit() {
    this.news.getStories().subscribe({
      next: (data) => {
        this.stories = data;
      },
      error: (err) => console.error(err)
    });
  }

  openStory(id: number) {
    this.router.navigate(['/dashboard', id]);
  }
}