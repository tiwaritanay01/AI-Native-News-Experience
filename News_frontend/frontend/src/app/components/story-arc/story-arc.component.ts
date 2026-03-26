import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector:'app-story-arc',
  standalone:true,
  imports:[CommonModule],
  template:`
  <div *ngIf="timeline && !timeline.loading && !timeline.error">
    <h3 class="text-sm font-bold uppercase tracking-widest text-purple-400 mb-4">Story Timeline</h3>

    <!-- Handle array of events -->
    <ul *ngIf="isArray(timeline)" class="space-y-2">
      <li *ngFor="let event of timeline" class="flex gap-3 p-3 rounded-lg bg-slate-700/30">
        <div class="flex-shrink-0 rounded-full bg-purple-500 mt-2" style="width: 8px; height: 8px;"></div>
        <span class="text-xs text-slate-300">{{ event }}</span>
      </li>
    </ul>

    <!-- Handle string response -->
    <div *ngIf="isString(timeline)" class="p-3 rounded-lg bg-slate-700/30">
      <p class="text-xs text-slate-300 whitespace-pre-wrap">{{ timeline }}</p>
    </div>

    <!-- Handle object response (e.g. {cluster_id: 0, timeline: "..."}) -->
    <div *ngIf="!isArray(timeline) && !isString(timeline)" class="p-3 rounded-lg bg-slate-700/30">
      <p class="text-xs text-slate-300 whitespace-pre-wrap">{{ getTimelineText() }}</p>
    </div>
  </div>

  <div *ngIf="timeline?.loading" class="flex items-center justify-center h-full">
    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-500"></div>
    <span class="text-xs text-slate-500 ml-2">Tracing story arc...</span>
  </div>

  <div *ngIf="timeline?.error" class="text-rose-400 text-sm">
    ⚠️ {{ timeline.error }}
  </div>
  `
})
export class StoryArcComponent {
  @Input() timeline: any;

  isArray(val: any): boolean {
    return Array.isArray(val);
  }

  isString(val: any): boolean {
    return typeof val === 'string';
  }

  getTimelineText(): string {
    if (!this.timeline) return '';
    if (this.timeline.timeline) {
      if (typeof this.timeline.timeline === 'string') return this.timeline.timeline;
      if (Array.isArray(this.timeline.timeline)) return this.timeline.timeline.join('\n');
    }
    if (this.timeline.raw) return this.timeline.raw;
    if (this.timeline.summary) return this.timeline.summary;
    const { loading, error, ...data } = this.timeline;
    return JSON.stringify(data, null, 2);
  }
}