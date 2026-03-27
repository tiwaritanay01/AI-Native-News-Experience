import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-story-arc',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="timeline && !timeline.loading && !timeline.error" class="space-y-6">
      <div *ngFor="let event of getEvents(); let i = index" class="flex gap-4 group">
        <div class="flex flex-col items-center">
          <div class="w-2 h-2 rounded-full border border-primary-container/40 group-hover:bg-primary-container group-hover:scale-125 transition-all shadow-[0_0_8px_rgba(242,202,80,0.3)]"></div>
          <div *ngIf="i < getEvents().length - 1" class="w-px flex-1 bg-primary-container/10 my-2 group-hover:bg-primary-container/30"></div>
        </div>
        <div class="pb-6">
          <div class="text-[0.625rem] text-primary-container/40 font-mono uppercase tracking-[0.2em] mb-1">Sequence node {{ i + 1 }}</div>
          <p class="font-body text-sm text-on-surface opacity-70 group-hover:opacity-100 transition-opacity italic leading-relaxed">
            {{ event }}
          </p>
        </div>
      </div>
      
      <div *ngIf="getEvents().length === 0" class="flex flex-col items-center p-8 border border-dashed border-outline-variant/30">
        <span class="text-[0.65rem] font-mono text-primary-container/30 uppercase italic">No sequence data recovered.</span>
      </div>
    </div>

    <div *ngIf="timeline?.loading" class="flex flex-col items-center py-12 gap-4">
      <div class="w-1 h-12 bg-primary-container/10 relative overflow-hidden">
        <div class="absolute inset-0 bg-primary-container/60 animate-[pulse_1.5s_infinite]"></div>
      </div>
      <span class="text-[0.625rem] font-mono text-primary-container/30 uppercase tracking-widest">Tracing Arc...</span>
    </div>

    <div *ngIf="timeline?.error" class="text-tertiary-container text-[0.625rem] font-mono p-4 uppercase border border-tertiary-container/30 italic">
      ERR: ARC_TRACER_TIMEOUT // {{ timeline.error }}
    </div>
  `,
  styles: [`
    :host { display: block; }
  `]
})
export class StoryArcComponent {
  @Input() timeline: any;

  getEvents(): string[] {
    if (!this.timeline) return [];
    if (Array.isArray(this.timeline)) return this.timeline;
    if (this.timeline.timeline) {
      if (Array.isArray(this.timeline.timeline)) return this.timeline.timeline;
      if (typeof this.timeline.timeline === 'string') return this.timeline.timeline.split('\n').filter((s: string) => s.trim());
    }
    if (typeof this.timeline === 'string') return this.timeline.split('\n').filter((s: string) => s.trim());
    return [];
  }
}