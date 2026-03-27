import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';
import { SidebarNavigationComponent } from '../sidebar-navigation/sidebar-navigation.component';

@Component({
  selector: 'app-video-studio',
  standalone: true,
  imports: [CommonModule, SidebarNavigationComponent],
  template: `
    <div class="flex h-screen bg-background text-on-background overflow-hidden font-body ml-20">
      <app-sidebar-navigation></app-sidebar-navigation>
      
      <main class="flex-1 overflow-auto p-8 no-scrollbar bg-surface-container-lowest">
        <header class="mb-12">
          <div class="flex items-center gap-4 mb-2">
            <span class="material-symbols-outlined text-primary text-3xl">video_library</span>
            <h1 class="font-headline text-5xl italic font-bold text-primary">Cinematic News Studio</h1>
          </div>
          <p class="text-primary-container/60 font-mono text-[0.65rem] uppercase tracking-[0.2em]">HuggingFace-Cinematic Generation Engine v1.0</p>
        </header>

        <section class="max-w-5xl mx-auto">
          <div class="glass-card border border-primary-container/10 p-12 text-center">
            <div *ngIf="loading" class="space-y-8">
              <div class="w-16 h-16 border-t-2 border-primary-container animate-spin rounded-full mx-auto"></div>
              <p class="font-mono text-xs text-primary-container/40 uppercase tracking-widest">Rendering Cinematic Storyboard...</p>
            </div>

            <div *ngIf="!loading && videoData" class="text-left space-y-8 animate-in fade-in duration-700">
               <div class="relative aspect-video bg-on-surface/5 border border-outline-variant/20 flex items-center justify-center group overflow-hidden">
                 <img src="https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&q=80&w=1200" 
                      class="absolute inset-0 w-full h-full object-cover opacity-30 group-hover:scale-105 transition-transform duration-1000" alt="Video Preview">
                 <button class="z-10 bg-primary/20 backdrop-blur-md border border-primary/40 text-primary w-20 h-20 rounded-full flex items-center justify-center hover:bg-primary/40 transition-all">
                   <span class="material-symbols-outlined scale-[2]">play_arrow</span>
                 </button>
                 <div class="absolute bottom-4 left-6 z-10 text-[0.6rem] font-mono text-primary-container/60 uppercase tracking-tighter">Sequence_ID: {{ videoData.engine }}_STB492</div>
               </div>

               <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                 <div *ngFor="let frame of videoData.frames" class="bg-surface-container-low p-4 border-l border-primary-container/40 transition-colors hover:border-primary">
                    <div class="text-[0.65rem] font-mono text-secondary-container mb-1 tracking-widest">{{ frame.timestamp }}</div>
                    <p class="text-xs text-on-surface opacity-70 leading-relaxed italic">{{ frame.description }}</p>
                 </div>
               </div>
               
               <div class="pt-8 border-t border-outline-variant/10 flex justify-between items-center">
                 <button class="bg-primary-container text-on-primary px-8 py-2.5 text-sm font-bold border-none hover:brightness-110 transition-all">EXPORT CINEMATIC PLAN</button>
                 <span class="text-[0.65rem] font-mono text-primary-container/30 uppercase italic">Validated via HF_TOKEN API</span>
               </div>
            </div>

            <div *ngIf="!loading && !videoData" class="space-y-6">
               <span class="material-symbols-outlined text-7xl text-primary-container/10">movie_creation</span>
               <h3 class="text-2xl font-headline text-on-surface italic">Select a news cluster to generate video</h3>
               <button (click)="generate()" class="mt-4 px-10 py-3 border border-primary-container/30 text-primary-container font-bold hover:bg-primary-container/10 transition-all uppercase tracking-widest text-xs">Initialize Studio</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  `,
  styles: [`:host { display: block; }`]
})
export class VideoStudioComponent implements OnInit {
  news = inject(NewsService);
  loading = false;
  videoData: any = null;

  ngOnInit() {}

  generate() {
    this.loading = true;
    // We assume cluster 0 for story of day or current active cluster
    this.news.getStoryVideo(0).subscribe({
      next: (data) => {
        this.videoData = data;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
      }
    });
  }
}