import { Component, inject, OnInit } from '@angular/core';
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
    <div class="flex h-screen bg-slate-950 overflow-hidden">
      <!-- Sidebar -->
      <app-sidebar-navigation></app-sidebar-navigation>

      <!-- Main Content -->
      <div class="flex-1 overflow-auto">
        <div class="min-h-screen p-8 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
          
          <!-- Header -->
          <div class="mb-8">
            <div class="flex justify-between items-center text-white">
              <div>
                <h1 class="text-3xl font-bold mb-2">AI-Native News Experience</h1>
                <p class="text-slate-400">Streaming Real-Time TPU Insights (JAX-Accelerated)</p>
              </div>
              <div class="text-right text-slate-400 text-sm">
                <div>{{ getCurrentTime() }}</div>
                <div class="flex items-center gap-2 justify-end mt-1">
                  <span class="w-2 h-2 rounded-full" [class.bg-blue-500]="loading" [class.bg-emerald-500]="!loading && !error"></span>
                  {{ loading ? 'TPU Core Generating...' : 'Analysis Ready' }}
                </div>
              </div>
            </div>
          </div>

          <!-- Sequential Bento Box Grid -->
          <div class="dashboard-grid grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Hero Card (Static Content First) -->
            <div class="lg:col-span-2">
               <app-hero-card></app-hero-card>
            </div>

            <!-- Why Matters Card (Streams Briefing) -->
            <div class="relative min-h-[250px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-4">
                <div *ngIf="!dashboard?.briefing && loading" class="absolute inset-0 flex items-center justify-center bg-slate-900/80 z-20">
                   <div class="text-center">
                      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                      <p class="text-xs text-slate-500">TPU Connection Established...</p>
                   </div>
                </div>
                <!-- Pass the streaming text to the component -->
                <app-why-matters-card [relevance]="{summary: dashboard?.briefingStream}"></app-why-matters-card>
            </div>

            <!-- Impact Radar Card (Lazy Loaded) -->
            <div class="lg:col-span-2 relative min-h-[300px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-6">
                 <div *ngIf="!dashboard?.impact" class="absolute inset-0 flex items-center justify-center bg-slate-900/40 z-10 backdrop-blur-sm">
                    <button (click)="loadImpact()" class="px-6 py-2 bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 rounded-full hover:bg-emerald-500/30 transition-all font-medium">
                       Analyze Market Impact
                    </button>
                 </div>
                 <app-impact-radar-card [impact]="dashboard?.impact"></app-impact-radar-card>
            </div>

            <!-- Contrarian Card (Lazy Loaded) -->
            <div class="relative min-h-[300px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-6">
                 <div *ngIf="!dashboard?.opinions" class="absolute inset-0 flex items-center justify-center bg-slate-900/40 z-10 backdrop-blur-sm">
                    <button (click)="loadOpinions()" class="px-6 py-2 bg-orange-500/20 border border-orange-500/40 text-orange-400 rounded-full hover:bg-orange-500/30 transition-all font-medium">
                       Compute Bull/Bear Sentiment
                    </button>
                 </div>
                 <app-contrarian-card [opinions]="dashboard?.opinions"></app-contrarian-card>
            </div>
            
            <!-- Story Arc (Lazy Loaded) -->
            <div class="lg:col-span-3 relative min-h-[300px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-6">
                <div *ngIf="!dashboard?.timeline" class="absolute inset-0 flex items-center justify-center bg-slate-900/40 z-10 backdrop-blur-sm">
                    <button (click)="loadTimeline()" class="px-6 py-2 bg-purple-500/20 border border-purple-500/40 text-purple-400 rounded-full hover:bg-purple-500/30 transition-all font-medium">
                       Trace Story Arc Timeline
                    </button>
                 </div>
                <app-story-arc [timeline]="dashboard?.timeline"></app-story-arc>
            </div>

          </div>

          <!-- Error Feedback -->
          <div *ngIf="error" class="mt-8 p-4 bg-rose-500/10 border border-rose-500/20 rounded-lg text-rose-400 text-sm">
             ⚠️ <b>Streaming Error:</b> {{ error }}
             <button (click)="initiateStreamingBriefing()" class="underline ml-2">Reconnect to TPU Core</button>
          </div>

        </div>
      </div>
    </div>
  `,
  styleUrl: '../../app.css'
})
export class DashboardLayoutComponent implements OnInit {
  route = inject(ActivatedRoute);
  news = inject(NewsService);
  streamer = inject(AgentStreamingService);
  stateService = inject(DashboardStateService);

  clusterId!: number;
  dashboard: any = {
      briefing: null,
      briefingStream: '',
      impact: null,
      opinions: null,
      timeline: null
  };
  loading = false;
  error: string | null = null;

  getCurrentTime(): string {
    return new Date().toLocaleTimeString('en-US', {
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
  }

  ngOnInit() {
    this.clusterId = Number(this.route.snapshot.paramMap.get('id') || 0);
    this.initiateStreamingBriefing();
  }

  initiateStreamingBriefing() {
    this.loading = true;
    this.error = null;
    this.dashboard.briefingStream = '';

    this.streamer.streamAgentResponse(this.clusterId, 'Generate a real-time news briefing.')
      .subscribe({
        next: (chunk) => {
          this.dashboard.briefingStream += chunk;
        },
        error: (err) => {
          this.error = "TPU Access Denied / JAX Initialization Failed.";
          console.error("Agent Streaming Failed:", err);
          this.loading = false;
        },
        complete: () => {
          this.loading = false;
          this.dashboard.briefing = { summary: this.dashboard.briefingStream };
        }
      });
  }

  async loadImpact() {
    // Lazy load logic: Triggered on user action
    this.dashboard.impact = { loading: true };
    const res = await this.news.getImpact(this.clusterId).toPromise();
    this.dashboard.impact = res;
  }

  async loadOpinions() {
    this.dashboard.opinions = { loading: true };
    const res = await this.news.getOpinions(this.clusterId).toPromise();
    this.dashboard.opinions = res;
  }

  async loadTimeline() {
    this.dashboard.timeline = { loading: true };
    const res = await this.news.getTimeline(this.clusterId).toPromise();
    this.dashboard.timeline = res;
  }

  retry() {
    this.initiateStreamingBriefing();
  }
}