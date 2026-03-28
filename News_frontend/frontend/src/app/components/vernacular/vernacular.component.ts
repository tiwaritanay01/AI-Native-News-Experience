import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';
import { SidebarNavigationComponent } from '../sidebar-navigation/sidebar-navigation.component';

@Component({
  selector: 'app-vernacular',
  standalone: true,
  imports: [CommonModule, SidebarNavigationComponent],
  template: `
    <div class="flex h-screen bg-background text-on-background overflow-hidden font-body ml-20">
      <app-sidebar-navigation></app-sidebar-navigation>
      
      <main class="flex-1 overflow-auto p-8 no-scrollbar bg-surface-container-lowest">
        <header class="mb-12">
          <div class="flex items-center gap-4 mb-2">
            <span class="material-symbols-outlined text-secondary-container text-3xl">translate</span>
            <h1 class="font-headline text-5xl italic font-bold text-on-surface">Vernacular Engine</h1>
          </div>
          <p class="text-secondary-container/60 font-mono text-[0.65rem] uppercase tracking-[0.2em]">JAX-Optimized Translation Hub (Gemini enabled)</p>
        </header>

        <section class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6">
           <!-- Language Selector -->
           <div class="lg:col-span-4 bg-surface-container-low border border-outline-variant/10 p-6 flex flex-col gap-6">
              <h3 class="font-headline text-2xl italic text-on-surface">Target Dialect</h3>
              <div class="grid grid-cols-2 gap-3">
                 <button *ngFor="let l of languages" 
                         (click)="selectLanguage(l)"
                         [class.bg-secondary-container]="selectedLanguage === l"
                         [class.text-on-secondary]="selectedLanguage === l"
                         [class.bg-surface-container-high]="selectedLanguage !== l"
                         class="px-4 py-3 text-xs font-mono uppercase transition-all tracking-widest border border-outline-variant/20 hover:ring-1 hover:ring-secondary-container">
                    {{ l }}
                 </button>
              </div>
              <div class="mt-auto pt-6 border-t border-outline-variant/10">
                 <button (click)="translate()" 
                         [disabled]="loading"
                         class="w-full bg-on-background text-background px-8 py-3 text-sm font-bold border-none hover:bg-secondary-container hover:text-on-secondary transition-all uppercase tracking-[0.2em] relative overflow-hidden">
                   {{ loading ? 'ENCODING...' : 'INITIALIZE VERNACULAR' }}
                 </button>
              </div>
           </div>

           <!-- Content Preview -->
           <div class="lg:col-span-8 glass-card border border-secondary-container/10 p-12 min-h-[400px] flex flex-col justify-center text-center">
              <div *ngIf="loading" class="space-y-4">
                 <div class="flex justify-center gap-1 h-2">
                   <div class="w-12 h-full bg-secondary-container animate-pulse"></div>
                   <div class="w-8 h-full bg-secondary-container/40 animate-pulse delay-75"></div>
                   <div class="w-16 h-full bg-secondary-container/10 animate-pulse delay-150"></div>
                 </div>
                 <p class="font-mono text-[0.6rem] text-secondary-container/40 uppercase tracking-[0.3em]">Decoding JAX tensors into {{ selectedLanguage }} dialect...</p>
              </div>

              <div *ngIf="!loading && translation" class="text-left animate-in slide-in-from-bottom duration-500">
                 <div class="flex items-center gap-2 mb-6">
                    <span class="text-[0.6rem] font-mono text-secondary-container border border-secondary-container/30 px-2 py-0.5 uppercase tracking-widest">{{ selectedLanguage }} Mode</span>
                    <div class="h-px flex-1 bg-outline-variant/10"></div>
                 </div>
                 <p class="font-body text-2xl text-on-surface leading-snug italic opacity-95 first-letter:text-4xl first-letter:font-headline first-letter:text-secondary-container">
                   {{ translation }}
                 </p>
                 <div class="mt-12 flex gap-4">
                   <button class="bg-secondary-container/10 text-secondary-container px-6 py-2 text-[0.6rem] font-bold border border-secondary-container/30 hover:bg-secondary-container/20 transition-all uppercase tracking-widest">PUBLISH TO REGIONAL FEED</button>
                   <button class="text-on-surface-variant font-mono text-[0.6rem] p-2 hover:underline uppercase">Copy Fragment</button>
                 </div>
              </div>

              <div *ngIf="!loading && !translation" class="opacity-30 flex flex-col items-center gap-6">
                 <span class="material-symbols-outlined text-8xl">auto_stories</span>
                 <p class="text-xs font-mono uppercase tracking-[0.2em]">Select dialect and trigger the engine to view localized news</p>
              </div>
           </div>
        </section>
      </main>
    </div>
  `,
  styles: [`:host { display: block; }`]
})
export class VernacularComponent {
  news = inject(NewsService);
  loading = false;
  translation: any = null;
  selectedLanguage = "Hindi";
  languages = ["Hindi", "Marathi", "Tamil", "Telugu", "Bengali", "Kannada", "Malayalam", "Gujarati"];

  selectLanguage(lang: string) {
    this.selectedLanguage = lang;
    this.translation = null;
  }

  translate() {
    this.loading = true;
    this.news.getStoryTranslation(0, this.selectedLanguage).subscribe({
      next: (data) => {
        this.translation = data.translated;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
      }
    });
  }
}