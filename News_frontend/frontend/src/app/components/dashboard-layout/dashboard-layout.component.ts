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
                <p class="text-slate-400">Loading AI Insights Sequentialy to Protect Hardware...</p>
              </div>
              <div class="text-right text-slate-400 text-sm">
                <div>{{ getCurrentTime() }}</div>
                <div class="flex items-center gap-2 justify-end mt-1">
                  <span class="w-2 h-2 rounded-full" [class.bg-blue-500]="loading" [class.bg-emerald-500]="!loading && !error"></span>
                  {{ loading ? 'Agents Processing...' : 'Analysis Ready' }}
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

            <!-- Why Matters Card (Loads after Basic Info) -->
            <div class="relative min-h-[250px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-4">
                <div *ngIf="!dashboard?.briefing && loading" class="absolute inset-0 flex items-center justify-center bg-slate-900/80 z-20">
                   <div class="text-center">
                      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                      <p class="text-xs text-slate-500">Generating Briefing...</p>
                   </div>
                </div>
                <app-why-matters-card [relevance]="dashboard?.briefing"></app-why-matters-card>
            </div>

            <!-- Impact Radar Card (Sequentially Loaded) -->
            <div class="lg:col-span-2 relative min-h-[300px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-4">
                 <div *ngIf="!dashboard?.impact && loading" class="absolute inset-0 flex items-center justify-center bg-slate-900/80 z-20">
                   <div class="text-center">
                      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mx-auto mb-2"></div>
                      <p class="text-xs text-slate-500">Decoding Market Impact...</p>
                   </div>
                </div>
                <app-impact-radar-card [impact]="dashboard?.impact"></app-impact-radar-card>
            </div>

            <!-- Contrarian Card (Sequentially Loaded) -->
            <div class="relative min-h-[300px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-4">
                 <div *ngIf="!dashboard?.opinions && loading" class="absolute inset-0 flex items-center justify-center bg-slate-900/80 z-20">
                   <div class="text-center">
                      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto mb-2"></div>
                      <p class="text-xs text-slate-500">Analyzing Bull/Bear Views...</p>
                   </div>
                </div>
                <app-contrarian-card [opinions]="dashboard?.opinions"></app-contrarian-card>
            </div>
            
            <!-- Story Arc (Sequentially Loaded) -->
            <div class="lg:col-span-3 relative min-h-[300px] bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden p-4">
                <div *ngIf="!dashboard?.timeline && loading" class="absolute inset-0 flex items-center justify-center bg-slate-900/80 z-20">
                   <div class="text-center">
                      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500 mx-auto mb-2"></div>
                      <p class="text-xs text-slate-500">Tracing Story Arc...</p>
                   </div>
                </div>
                <app-story-arc [timeline]="dashboard?.timeline"></app-story-arc>
            </div>

          </div>

          <!-- Error Feedback -->
          <div *ngIf="error" class="mt-8 p-4 bg-rose-500/10 border border-rose-500/20 rounded-lg text-rose-400 text-sm">
             ⚠️ <b>Sequence Throttled:</b> {{ error }}
             <button (click)="retry()" class="underline ml-2">Resume Next Agent</button>
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
  stateService = inject(DashboardStateService);

  clusterId!: number;
  dashboard: any = {
      briefing: null,
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
    this.startSequentialLoading();
  }

  async startSequentialLoading() {
    this.loading = true;
    this.error = null;

    try {
      // Step 1: Loading Briefing (First Priority)
      const briefingRes = await this.news.getBriefing(this.clusterId).toPromise();
      this.dashboard.briefing = briefingRes;
      
      // Step 2: Market Impact (Second Priority) - wait a moment for CPU
      await new Promise(r => setTimeout(r, 1500));
      const impactRes = await this.news.getImpact(this.clusterId).toPromise();
      this.dashboard.impact = impactRes;

      // Step 3: Contrarian Opinions
      await new Promise(r => setTimeout(r, 1500));
      const opinionsRes = await this.news.getOpinions(this.clusterId).toPromise();
      this.dashboard.opinions = opinionsRes;

      // Step 4: Story Arc Timeline
      await new Promise(r => setTimeout(r, 1500));
      const timelineRes = await this.news.getTimeline(this.clusterId).toPromise();
      this.dashboard.timeline = timelineRes;

    } catch (err) {
      this.error = "Hardware Protection Initiated / AI Connection Issue.";
      console.error("AI Sequential Load Failed:", err);
    } finally {
      this.loading = false;
    }
  }

  retry() {
    this.startSequentialLoading();
  }
}