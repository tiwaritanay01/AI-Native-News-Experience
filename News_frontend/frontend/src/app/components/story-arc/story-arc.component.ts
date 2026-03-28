import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-story-arc',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="timeline && !timeline.loading && !timeline.error" class="space-y-8 animate-in fade-in duration-1000">
      
      <!-- Chronological Timeline -->
      <section class="space-y-6">
        <h3 class="text-[0.6rem] font-mono text-primary uppercase tracking-[0.3em] mb-4 border-b border-primary/10 pb-2 italic">Chronological Arc</h3>
        <div *ngFor="let event of getEvents(); let i = index" class="flex gap-6 group">
          <div class="flex flex-col items-center">
            <div class="w-1.5 h-1.5 rounded-full bg-primary-container/20 group-hover:bg-primary group-hover:scale-150 transition-all border border-primary/40"></div>
            <div *ngIf="i < getEvents().length - 1" class="w-px flex-1 bg-primary/10 my-1 group-hover:bg-primary/30"></div>
          </div>
          <div class="pb-6">
            <div class="text-[0.55rem] text-primary/40 font-mono uppercase tracking-tighter mb-1">{{ event.date || 'Sequence_' + (i+1) }}</div>
            <p class="font-body text-xs text-on-surface/80 group-hover:text-on-surface transition-colors leading-relaxed italic pr-4">
              {{ event.event || event }}
            </p>
          </div>
        </div>
      </section>

      <!-- Sentiment Arc -->
      <section *ngIf="timeline.sentiment_arc" class="p-6 bg-primary/5 border border-primary/10 flex flex-col gap-2">
         <h4 class="text-[0.55rem] font-mono text-primary/60 uppercase tracking-widest italic">Sentiment Trajectory</h4>
         <p class="text-[0.65rem] font-body text-on-surface italic">{{ timeline.sentiment_arc }}</p>
      </section>

      <!-- Future Predictions -->
      <section *ngIf="getPredictions().length > 0">
        <h3 class="text-[0.6rem] font-mono text-secondary-container uppercase tracking-[0.3em] mb-4 border-b border-secondary-container/10 pb-2 italic text-primary">Strategic Forecast</h3>
        <div class="grid grid-cols-1 gap-4">
           <div *ngFor="let pred of getPredictions(); let i = index" 
                class="p-4 bg-surface-container-high border-l border-primary/40 flex items-start gap-4 hover:border-primary transition-all group">
              <span class="text-[0.6rem] font-mono text-primary/40 group-hover:text-primary">PRED_0{{ i+1 }}</span>
              <p class="text-[0.65rem] text-on-surface italic leading-snug">{{ pred }}</p>
           </div>
        </div>
      </section>
    </div>

    <!-- Loading/Error states same as before -->
    <div *ngIf="timeline?.loading" class="flex flex-col items-center py-12 gap-4">
      <div class="w-1 h-12 bg-primary/10 relative overflow-hidden">
        <div class="absolute inset-0 bg-primary/60 animate-[pulse_1.5s_infinite]"></div>
      </div>
      <span class="text-[0.625rem] font-mono text-primary/30 uppercase tracking-widest italic animate-pulse">Syncing Narrative Tensors...</span>
    </div>

    <div *ngIf="timeline?.error" class="text-error-container text-[0.6rem] font-mono p-4 uppercase border border-error-container/30 italic glass-card">
      ERR: ARC_TRACER_TIMEOUT // {{ timeline.error }}
    </div>
  `,
  styles: [`:host { display: block; }`]
})
export class StoryArcComponent {
  @Input() timeline: any;

  getEvents(): any[] {
    if (!this.timeline) return [];
    if (this.timeline.events) return this.timeline.events;
    // Fallback for old format
    if (Array.isArray(this.timeline)) return this.timeline;
    if (this.timeline.timeline && Array.isArray(this.timeline.timeline)) return this.timeline.timeline;
    return [];
  }

  getPredictions(): string[] {
    if (!this.timeline) return [];
    return this.timeline.predictions || [];
  }
}