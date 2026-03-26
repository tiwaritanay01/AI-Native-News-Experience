import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector:'app-impact-radar-card',
  standalone:true,
  imports:[CommonModule],
  template:`
  <div *ngIf="impact && !impact.loading && !impact.error">
    <h3 class="text-sm font-bold uppercase tracking-widest text-emerald-400 mb-4">Impact Radar</h3>
    
    <div class="space-y-3">
      <div class="flex gap-3 p-3 rounded-lg bg-slate-700/30">
        <div class="flex-shrink-0 rounded-full bg-emerald-500 mt-2" style="width: 8px; height: 8px;"></div>
        <div class="flex-1">
          <b class="text-slate-200 text-sm">Cluster ID</b>
          <p class="text-xs text-slate-400">{{ impact?.cluster_id }}</p>
        </div>
      </div>
      <div class="flex gap-3 p-3 rounded-lg bg-slate-700/30">
        <div class="flex-shrink-0 rounded-full bg-blue-500 mt-2" style="width: 8px; height: 8px;"></div>
        <div class="flex-1">
          <b class="text-slate-200 text-sm">Analysis</b>
          <p class="text-xs text-slate-400 whitespace-pre-wrap">{{ getImpactText() }}</p>
        </div>
      </div>
    </div>
  </div>

  <div *ngIf="impact?.loading" class="flex items-center justify-center h-full">
    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-emerald-500"></div>
    <span class="text-xs text-slate-500 ml-2">Analyzing impact...</span>
  </div>

  <div *ngIf="impact?.error" class="text-rose-400 text-sm">
    ⚠️ {{ impact.error }}
  </div>
  `
})
export class ImpactRadarCardComponent {
  @Input() impact: any;

  getImpactText(): string {
    if (!this.impact) return '';
    // Handle various response shapes from the backend
    if (typeof this.impact === 'string') return this.impact;
    if (this.impact.impact) {
      if (typeof this.impact.impact === 'string') return this.impact.impact;
      if (this.impact.impact.raw) return this.impact.impact.raw;
      return JSON.stringify(this.impact.impact, null, 2);
    }
    if (this.impact.raw) return this.impact.raw;
    if (this.impact.summary) return this.impact.summary;
    return JSON.stringify(this.impact, null, 2);
  }
}