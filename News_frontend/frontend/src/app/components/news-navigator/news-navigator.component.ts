import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';
import { Router } from '@angular/router';
import { SidebarNavigationComponent } from '../sidebar-navigation/sidebar-navigation.component';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-news-navigator',
  standalone: true,
  imports: [CommonModule, SidebarNavigationComponent, FormsModule],
  template: `
    <div class="flex h-screen bg-background text-on-background overflow-hidden font-body ml-20">
      <app-sidebar-navigation></app-sidebar-navigation>
      
      <main class="flex-1 overflow-auto p-8 no-scrollbar bg-surface-container-lowest">
        <header class="mb-12 flex justify-between items-end">
          <div>
            <div class="flex items-center gap-4 mb-2">
              <span class="material-symbols-outlined text-primary text-3xl">explore</span>
              <h1 class="font-headline text-5xl italic font-bold text-primary">Intelligence Navigator</h1>
            </div>
            <p class="text-primary-container/60 font-mono text-[0.65rem] uppercase tracking-[0.2em] italic">Active JAX Intelligence Clustering Signal: Stable (Groq-Llama Accelerated)</p>
          </div>
          
          <div class="flex gap-4">
            <button (click)="openUniversalChat()" class="px-6 py-2 border border-primary/20 text-primary font-mono text-[0.6rem] uppercase tracking-widest hover:bg-primary/5">Launch Universal Chat</button>
          </div>
        </header>

        <section class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
          <div *ngFor="let story of stories; let i = index" 
               class="glass-card border border-primary-container/10 p-6 flex flex-col gap-4 group hover:border-primary/40 transition-all hover:-translate-y-1 relative">
            
            <div class="flex justify-between items-start">
               <span class="text-[0.625rem] font-mono text-primary-container/40 uppercase tracking-widest italic">Node_{{ story.cluster_id }}</span>
               <div class="w-1.5 h-1.5 rounded-full bg-secondary-container animate-pulse"></div>
            </div>

            <h3 class="font-headline text-xl font-bold leading-tight italic">
              {{ story.title }}
            </h3>
            
            <p class="text-xs text-on-surface/70 line-clamp-3 leading-relaxed first-letter:text-lg first-letter:font-headline first-letter:text-primary">
              {{ story.summary }}
            </p>

            <div class="mt-auto pt-6 border-t border-outline-variant/10 flex justify-between items-center bg-surface-container-lowest/50">
               <button (click)="openStory(story.cluster_id)" class="text-[0.6rem] font-bold uppercase tracking-widest text-primary hover:underline">Deep Intelligence Panel</button>
               <button (click)="startNavigatorChat(story)" class="flex items-center gap-2 text-[0.6rem] font-mono text-primary/40 hover:text-primary transition-colors border border-primary/10 px-2 py-1">
                 <span class="material-symbols-outlined text-sm">chat_bubble</span>
                 NAVIGATE
               </button>
            </div>
          </div>
        </section>
      </main>

      <!-- Chat Sidebar -->
      <div *ngIf="showChat" class="fixed right-0 top-0 bottom-0 w-[450px] bg-surface-container-low border-l border-primary/20 shadow-2xl z-50 animate-in slide-in-from-right duration-500 backdrop-blur-xl bg-opacity-95 flex flex-col p-8">
        <div class="flex justify-between items-center mb-10 border-b border-primary/10 pb-6">
          <div>
            <h2 class="font-headline text-2xl font-bold italic text-primary">Navigator Intel</h2>
            <p class="text-[0.6rem] uppercase font-mono text-primary/40 tracking-widest">Story_ID: {{ activeStory?.cluster_id }} (Groq LLAMA-3.3)</p>
          </div>
          <button (click)="showChat = false" class="text-primary/40 hover:text-primary material-symbols-outlined">close</button>
        </div>

        <div class="flex-1 overflow-auto space-y-6 no-scrollbar pb-10">
          <div *ngFor="let msg of chatHistory" [class.text-right]="msg.role === 'user'">
            <div [class.bg-primary]="msg.role === 'user'" 
                 [class.text-on-primary]="msg.role === 'user'"
                 [class.bg-surface-container-high]="msg.role === 'assistant'"
                 [class.ml-auto]="msg.role === 'user'"
                 class="inline-block p-4 max-w-[90%] text-xs leading-relaxed transition-all">
              <span class="font-mono text-[0.55rem] uppercase block mb-1 opacity-50">{{ msg.role === 'user' ? 'Local_User' : 'Navigator_AI' }}</span>
              {{ msg.content }}
            </div>
          </div>
          <div *ngIf="chatLoading" class="animate-pulse flex items-center gap-2 text-[0.6rem] font-mono text-primary/40 border border-primary/10 w-fit p-2">
            <span class="w-1.5 h-1.5 rounded-full bg-primary animate-ping"></span>
            Syncing Tensors...
          </div>
        </div>

        <div class="mt-auto relative">
          <input [(ngModel)]="currentQuestion" 
                 (keyup.enter)="sendMessage()" 
                 placeholder="Probe deeper into this cluster..." 
                 class="w-full bg-surface-container-high border border-primary/10 p-4 pr-12 text-xs focus:outline-none focus:border-primary/50 font-mono italic">
          <button (click)="sendMessage()" class="absolute right-4 top-1/2 -translate-y-1/2 text-primary hover:scale-110 active:scale-95 transition-all">
            <span class="material-symbols-outlined">send</span>
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`:host { display: block; }`]
})
export class NewsNavigatorComponent implements OnInit {
  news = inject(NewsService);
  router = inject(Router);
  http = inject(HttpClient);
  cdr = inject(ChangeDetectorRef);

  // Expose the API base URL from NewsService so chat uses ngrok, not localhost
  private get apiBase(): string { return (this.news as any).api; }
  private get ngrokHeaders(): HttpHeaders { return (this.news as any).headers; }

  stories: any[] = [];
  showChat = false;
  activeStory: any = null;
  chatHistory: any[] = [];
  currentQuestion = '';
  chatLoading = false;

  ngOnInit() {
    this.news.getStories().subscribe({
      next: (data) => this.stories = data,
      error: (err) => console.error(err)
    });
  }

  openStory(id: number) {
    this.router.navigate(['/dashboard', id]);
  }

  openUniversalChat() {
    this.activeStory = null;
    this.chatHistory = [{ role: 'assistant', content: 'Universal Navigator Standby... Cluster_Context: ALL.' }];
    this.showChat = true;
  }

  startNavigatorChat(story: any) {
    this.activeStory = story;
    this.chatHistory = [{ role: 'assistant', content: `Intelligence Sync Successful for Node_${story.cluster_id}. How shall we proceed?` }];
    this.showChat = true;
  }

  sendMessage() {
    if (!this.currentQuestion.trim()) return;

    const userMsg = { role: 'user', content: this.currentQuestion };
    this.chatHistory.push(userMsg);
    const question = this.currentQuestion;
    this.currentQuestion = '';
    this.chatLoading = true;
    this.cdr.detectChanges();

    // Use the same base URL as NewsService (supports ngrok tunnels)
    this.http.post(`${this.apiBase}/navigator/chat`, {
       cluster_id: this.activeStory?.cluster_id ?? 0,
       question: question,
       history: this.chatHistory.slice(-6)
    }, { headers: this.ngrokHeaders }).subscribe({
       next: (res: any) => {
         this.chatHistory.push({ role: 'assistant', content: res.response });
         this.chatLoading = false;
         this.cdr.detectChanges();
       },
       error: () => {
         this.chatLoading = false;
         this.chatHistory.push({ role: 'assistant', content: '⚠️ Node connection interrupted. Retrying routing tables...' });
         this.cdr.detectChanges();
       }
    });
  }
}