import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-sidebar-navigation',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <aside class="fixed left-0 top-0 h-screen w-20 flex flex-col border-r border-primary-container/20 bg-surface-container-lowest z-50">
      <!-- Logo -->
      <div class="h-14 flex items-center justify-center border-b border-primary-container/20">
        <span class="font-headline italic text-xl text-primary">A</span>
      </div>

      <!-- Nav Items -->
      <nav class="flex-1 flex flex-col items-center py-6 gap-8">
        <a routerLink="/dashboard" routerLinkActive="active-link"
           class="group flex flex-col items-center gap-1 w-full py-3 text-primary-container/40 hover:bg-primary-container/10 hover:text-primary transition-all">
          <span class="material-symbols-outlined">dashboard</span>
          <span class="font-label text-[0.625rem] tracking-[0.05rem] uppercase text-center px-1">Dashboard</span>
        </a>

        <a routerLink="/news-navigator" routerLinkActive="active-link"
           class="group flex flex-col items-center gap-1 w-full py-3 text-primary-container/40 hover:bg-primary-container/10 hover:text-primary transition-all">
          <span class="material-symbols-outlined">vertical_split</span>
          <span class="font-label text-[0.625rem] tracking-[0.05rem] uppercase text-center px-1">Navigator</span>
        </a>

        <a routerLink="/video-studio" routerLinkActive="active-link"
           class="group flex flex-col items-center gap-1 w-full py-3 text-primary-container/40 hover:bg-primary-container/10 hover:text-primary transition-all">
          <span class="material-symbols-outlined">video_library</span>
          <span class="font-label text-[0.625rem] tracking-[0.05rem] uppercase text-center px-1">Studio</span>
        </a>

        <a routerLink="/story-arc" routerLinkActive="active-link"
           class="group flex flex-col items-center gap-1 w-full py-3 text-primary-container/40 hover:bg-primary-container/10 hover:text-primary transition-all">
          <span class="material-symbols-outlined">auto_graph</span>
          <span class="font-label text-[0.625rem] tracking-[0.05rem] uppercase text-center px-1">Arc</span>
        </a>

        <a routerLink="/vernacular" routerLinkActive="active-link"
           class="group flex flex-col items-center gap-1 w-full py-3 text-primary-container/40 hover:bg-primary-container/10 hover:text-primary transition-all">
          <span class="material-symbols-outlined">translate</span>
          <span class="font-label text-[0.625rem] tracking-[0.05rem] uppercase text-center px-1">Vernacular</span>
        </a>
      </nav>

      <!-- Version Branding -->
      <div class="pb-6 flex flex-col items-center gap-4">
        <span class="font-label text-[0.6875rem] tracking-[0.1em] text-primary-container/40 rotate-180 [writing-mode:vertical-lr]">AUREUM V2.0</span>
      </div>
    </aside>
  `,
  styles: [`
    .active-link {
      color: var(--color-primary) !important;
      border-left: 2px solid var(--color-primary);
      background-color: #d4af3710;
    }
    .active-link .material-symbols-outlined {
      font-variation-settings: 'FILL' 1;
    }
  `]
})
export class SidebarNavigationComponent {}