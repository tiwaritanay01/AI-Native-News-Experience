import { Component, inject, OnInit, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { SidebarNavigationComponent } from '../sidebar-navigation/sidebar-navigation.component';
import { HeroCardComponent } from '../hero-card/hero-card.component';
import { WhyMattersCardComponent } from '../why-matters-card/why-matters-card.component';
import { ImpactRadarCardComponent } from '../impact-radar-card/impact-radar-card.component';
import { ContrarianCardComponent } from '../contrarian-card/contrarian-card.component';
import { StoryArcComponent } from '../story-arc/story-arc.component';
import { DashboardStateService } from '../../services/dashboard-state.service';
import { NewsService } from '../../services/news.service';
import { AgentStreamingService } from '../../services/agent-streaming.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard-layout',
  standalone: true,
  imports: [
    CommonModule,
    SidebarNavigationComponent,
    HeroCardComponent,
    WhyMattersCardComponent,
    ImpactRadarCardComponent,
    ContrarianCardComponent,
    StoryArcComponent
  ],
  template: `
    <div class="flex h-screen bg-background text-on-background overflow-hidden font-body">
      <!-- SideNavBar -->
      <app-sidebar-navigation></app-sidebar-navigation>

      <div class="flex-1 flex flex-col min-w-0 ml-20">
        <!-- TopAppBar -->
        <header class="sticky top-0 w-full z-40 flex justify-between items-center px-6 h-14 bg-background/80 backdrop-blur-xl border-b border-primary-container/15">
          <div class="flex items-center gap-8 flex-1">
            <span class="font-headline text-2xl italic text-primary">Aureum Terminal</span>
            <div class="relative w-96 max-w-md hidden md:block">
              <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary-container/40 text-sm font-light">search</span>
              <input class="w-full bg-white/5 border-none focus:ring-1 focus:ring-primary text-sm py-1.5 pl-10 text-on-surface placeholder:text-primary-container/30" 
                     placeholder="Search markets, news, or sectors..." type="text"/>
            </div>
          </div>
          <div class="flex items-center gap-6">
            <div class="flex gap-4">
              <button class="text-primary-container/60 hover:text-primary transition-colors"><span class="material-symbols-outlined">notifications</span></button>
              <button class="text-primary-container/60 hover:text-primary transition-colors"><span class="material-symbols-outlined">settings</span></button>
              <button class="text-primary-container/60 hover:text-primary transition-colors"><span class="material-symbols-outlined">account_circle</span></button>
            </div>
          </div>
        </header>

        <!-- Main Content Canvas -->
        <main class="flex-1 overflow-auto p-6 pb-20 no-scrollbar">
          <!-- Bento Grid Layout -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 auto-rows-min">
            
            <!-- Personalized Morning Briefing (Top Row - Span Full) -->
            <section class="lg:col-span-12 glass-card border border-on-secondary-container/30 p-8 relative overflow-hidden">
              <div class="absolute top-0 right-0 w-64 h-64 bg-secondary-container/5 blur-[100px]"></div>
              <div class="flex flex-col md:flex-row justify-between items-start gap-8 relative z-10">
                <div class="max-w-4xl">
                  <div class="flex items-center gap-2 mb-4">
                    <span class="text-secondary-container font-mono text-xs tracking-widest uppercase">
                      Intelligent Briefing • {{ currentTime }}
                    </span>
                    <div class="h-px flex-1 bg-on-secondary-container/20"></div>
                  </div>
                  
                  <app-hero-card></app-hero-card>

                  <div class="mt-8">
                     <app-why-matters-card 
                        [relevance]="dashboard.briefingStream" 
                        [isGenerating]="loading">
                     </app-why-matters-card>
                  </div>

                  <div class="flex gap-4 mt-8">
                    <button class="bg-primary-container text-on-primary px-6 py-2 text-sm font-bold border-none hover:brightness-110 transition-all">EXECUTE TRADE PLAN</button>
                    <button (click)="retry()" class="border border-outline-variant/30 text-primary px-6 py-2 text-sm font-bold hover:bg-white/5 transition-all uppercase tracking-tight">Reconnect TPU</button>
                  </div>
                </div>

                <div class="flex-shrink-0 w-full md:w-auto">
                  <div class="bg-surface-container-low p-4 border border-outline-variant/20">
                    <div class="text-[0.625rem] text-primary-container/50 font-mono uppercase mb-2 tracking-tighter">AI Pulse Check</div>
                    <div class="flex items-end gap-2">
                       <span class="text-3xl font-mono text-secondary-container leading-none" [class.animate-pulse]="loading">
                          {{ loading ? '...' : '94%' }}
                       </span>
                       <span class="text-xs font-mono text-secondary-container pb-1 uppercase">
                          {{ loading ? 'Computing' : 'Bullish' }}
                       </span>
                    </div>
                    <div class="mt-4 flex gap-1 h-1">
                      <div class="w-12 h-full bg-secondary-container"></div>
                      <div class="w-8 h-full bg-secondary-container"></div>
                      <div class="w-10 h-full bg-secondary-container/40"></div>
                      <div class="w-4 h-full bg-secondary-container/10"></div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- Middle Row - Left: Impact Radar -->
            <section class="lg:col-span-4 bg-surface-container-lowest p-6 flex flex-col border border-outline-variant/10">
              <div class="flex justify-between items-center mb-6">
                <h2 class="font-headline text-xl font-bold text-primary">Impact Radar</h2>
                <span class="font-mono text-[0.65rem] text-secondary-container border border-secondary-container/20 px-2 py-0.5" 
                      [class.animate-pulse]="dashboard.impact?.loading">
                  {{ dashboard.impact?.loading ? 'GENERATING...' : 'LIVE ANALYSIS' }}
                </span>
              </div>
              
              <div class="flex-1 relative min-h-[300px]">
                <div *ngIf="!dashboard.impact" class="absolute inset-0 flex items-center justify-center bg-surface-container-lowest/40 z-10 backdrop-blur-sm">
                   <button (click)="loadImpact()" class="px-6 py-2 bg-secondary-container/10 border border-secondary-container/30 text-secondary-container rounded-sm hover:bg-secondary-container/20 transition-all font-bold text-xs uppercase tracking-widest">
                      Initialize Radar
                   </button>
                </div>
                <app-impact-radar-card [impact]="dashboard.impact"></app-impact-radar-card>
              </div>
            </section>

            <!-- Middle Row - Center: Contrarian Opinions -->
            <section class="lg:col-span-4 bg-surface-container-low p-6 flex flex-col border border-outline-variant/10">
              <div class="flex items-center gap-2 mb-6">
                <span class="material-symbols-outlined text-primary text-lg">psychology_alt</span>
                <h2 class="font-headline text-xl font-bold text-on-surface">Contrarian Views</h2>
              </div>
              
              <div class="flex-1 relative min-h-[300px]">
                <div *ngIf="!dashboard.opinions" class="absolute inset-0 flex items-center justify-center bg-surface-container-low/40 z-10 backdrop-blur-sm">
                   <button (click)="loadOpinions()" class="px-6 py-2 bg-primary-container/10 border border-primary-container/30 text-primary-container rounded-sm hover:bg-primary-container/20 transition-all font-bold text-xs uppercase tracking-widest">
                      Compute Dilemma
                   </button>
                </div>
                <app-contrarian-card [opinions]="dashboard.opinions"></app-contrarian-card>
              </div>
            </section>

            <!-- Middle Row - Right: Story Arc -->
            <section class="lg:col-span-4 bg-surface-container-lowest p-6 border border-outline-variant/10">
               <div class="flex justify-between items-center mb-6">
                <h2 class="font-headline text-xl font-bold text-on-surface">Narrative Arc</h2>
                <button (click)="loadTimeline()" class="text-xs font-mono text-primary-container hover:text-primary transition-colors uppercase underline decoration-primary-container/30">
                  Trace Timeline
                </button>
              </div>
              
              <div class="relative min-h-[300px]">
                <div *ngIf="!dashboard.timeline" class="absolute inset-0 flex items-center justify-center bg-surface-container-lowest/40 z-10 backdrop-blur-sm">
                   <span class="text-[0.65rem] font-mono text-primary-container/40 uppercase">AWAITING SEQUENCE...</span>
                </div>
                <app-story-arc [timeline]="dashboard.timeline"></app-story-arc>
              </div>
            </section>

          </div>
        </main>

        <!-- Live Market Ticker -->
        <footer class="fixed bottom-0 left-0 w-full z-50 flex items-center overflow-hidden whitespace-nowrap bg-surface-container-lowest/90 backdrop-blur-md h-8 border-t border-primary-container/20 shadow-[0_-4px_12px_rgba(242,202,80,0.05)]">
          <div class="ticker-animate flex gap-12 items-center">
            <div class="flex items-center gap-2">
              <span class="font-mono text-[0.65rem] tracking-tighter text-on-surface-variant uppercase">S&P 500</span>
              <span class="material-symbols-outlined text-[14px] text-secondary-container">trending_up</span>
              <span class="font-mono text-[0.65rem] tracking-tighter text-secondary-container">5,421.22 (+1.2%)</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="font-mono text-[0.65rem] tracking-tighter text-on-surface-variant uppercase">NASDAQ</span>
              <span class="material-symbols-outlined text-[14px] text-secondary-container">trending_up</span>
              <span class="font-mono text-[0.65rem] tracking-tighter text-secondary-container">16,428.10 (+1.8%)</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="font-mono text-[0.65rem] tracking-tighter text-on-surface-variant uppercase">BTC/USD</span>
              <span class="material-symbols-outlined text-[14px] text-tertiary-container">trending_down</span>
              <span class="font-mono text-[0.65rem] tracking-tighter text-tertiary-container">71,402.50 (-0.4%)</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="font-mono text-[0.65rem] tracking-tighter text-on-surface-variant uppercase">GOLD</span>
              <span class="material-symbols-outlined text-[14px] text-secondary-container">trending_up</span>
              <span class="font-mono text-[0.65rem] tracking-tighter text-secondary-container">2,354.10 (+0.8%)</span>
            </div>
            <!-- Repeated for seamless loop -->
            <div class="flex items-center gap-2">
              <span class="font-mono text-[0.65rem] tracking-tighter text-on-surface-variant uppercase">S&P 500</span>
              <span class="material-symbols-outlined text-[14px] text-secondary-container">trending_up</span>
              <span class="font-mono text-[0.65rem] tracking-tighter text-secondary-container">5,421.22 (+1.2%)</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  `,
  styleUrl: '../../app.css'
})
export class DashboardLayoutComponent implements OnInit, OnDestroy {
  route = inject(ActivatedRoute);
  news = inject(NewsService);
  streamer = inject(AgentStreamingService);
  stateService = inject(DashboardStateService);
  cdr = inject(ChangeDetectorRef);

  clusterId!: number;
  dashboard: any = {
      briefingStream: '',
      impact: null,
      opinions: null,
      timeline: null
  };
  loading = false;
  error: string | null = null;
  currentTime = '';
  private clockInterval: any;
  private streamSub?: Subscription;

  ngOnInit() {
    this.clusterId = Number(this.route.snapshot.paramMap.get('id') || 0);
    this.updateClock();
    this.clockInterval = setInterval(() => { 
      this.currentTime = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit', minute: '2-digit', second: '2-digit'
      });
    }, 1000);
    this.initiateStreamingBriefing();
  }

  ngOnDestroy() {
    if (this.clockInterval) clearInterval(this.clockInterval);
    if (this.streamSub) this.streamSub.unsubscribe();
  }

  private updateClock() {
    this.currentTime = new Date().toLocaleTimeString('en-US', {
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
  }

  initiateStreamingBriefing() {
    this.loading = true;
    this.error = null;
    this.dashboard.briefingStream = '';

    this.streamSub = this.streamer.streamAgentResponse(this.clusterId, 'Generate a real-time news briefing.')
      .subscribe({
        next: (chunk) => {
          console.log('📡 TPU Token:', chunk);
          if (chunk === '[START]') {
            this.dashboard.briefingStream = '';
          } else {
            this.dashboard.briefingStream += chunk;
          }
          // CRITICAL: Force Angular change detection on each token
          this.cdr.detectChanges();
        },
        error: (err) => {
          this.error = "TPU Access Denied / JAX Initialization Failed.";
          console.error("Agent Streaming Failed:", err);
          this.loading = false;
          this.cdr.detectChanges();
        },
        complete: () => {
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
  }

  loadImpact() {
    this.dashboard.impact = { loading: true };
    this.cdr.detectChanges();
    this.news.getImpact(this.clusterId).subscribe({
      next: (res) => {
        this.dashboard.impact = res;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.dashboard.impact = { error: 'Failed to load impact data' };
        this.cdr.detectChanges();
      }
    });
  }

  loadOpinions() {
    this.dashboard.opinions = { loading: true };
    this.cdr.detectChanges();
    this.news.getOpinions(this.clusterId).subscribe({
      next: (res) => {
        this.dashboard.opinions = res;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.dashboard.opinions = { error: 'Failed to load opinions' };
        this.cdr.detectChanges();
      }
    });
  }

  loadTimeline() {
    this.dashboard.timeline = { loading: true };
    this.cdr.detectChanges();
    this.news.getTimeline(this.clusterId).subscribe({
      next: (res) => {
        this.dashboard.timeline = res;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.dashboard.timeline = { error: 'Failed to load timeline' };
        this.cdr.detectChanges();
      }
    });
  }

  retry() {
    this.initiateStreamingBriefing();
  }
}