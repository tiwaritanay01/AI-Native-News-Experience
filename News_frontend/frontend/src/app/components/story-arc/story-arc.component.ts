import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-story-arc',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="timeline && !timeline.loading && !timeline.error" class="space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-1000">
      
      <!-- Visual Sentiment Tracker -->
      <div class="px-4 py-3 bg-primary/5 border border-primary/20 flex flex-col gap-3 relative overflow-hidden group">
         <div class="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent"></div>
         <div class="flex justify-between items-center">
            <h4 class="text-[0.55rem] font-mono text-primary/80 uppercase tracking-widest italic flex items-center gap-2">
               Narrative Pulse
               <span class="inline-flex gap-1">
                  <span class="w-1 h-1 rounded-full bg-secondary-container animate-pulse shadow-[0_0_8px_rgba(19,255,67,0.5)]"></span>
                  <span class="w-1 h-1 rounded-full bg-secondary-container/40 animate-pulse delay-75"></span>
                  <span class="w-1 h-1 rounded-full bg-secondary-container/20 animate-pulse delay-150"></span>
               </span>
            </h4>
            <span class="text-[0.5rem] font-mono text-primary/40 uppercase">{{ timeline.sentiment_arc || 'Synchronizing Data' }}</span>
         </div>
         <div class="flex gap-1 h-2">
            <div *ngFor="let m of [1,2,3,4,5,6,7,8,9,10]" 
                 class="flex-1 bg-primary/10 rounded-sm group-hover:bg-primary/20 transition-all cursor-crosshair relative"
                 [style.opacity]="m/10">
                 <div *ngIf="m === 7" class="absolute inset-0 bg-primary/60 blur-[2px] animate-pulse"></div>
            </div>
         </div>
      </div>

      <!-- Chronological Arc -->
      <section class="space-y-6">
        <h3 class="text-[0.6rem] font-mono text-primary uppercase tracking-[0.3em] mb-4 border-b border-primary/10 pb-2 italic">Chronological Sequence</h3>
        
        <div *ngIf="getEvents().length === 0" class="py-8 text-center text-on-surface/30 font-mono text-[0.6rem] uppercase tracking-widest">
           {{ errorMessage }}
        </div>

        <div *ngFor="let event of getEvents(); let i = index" class="flex gap-6 group relative">
          <div class="flex flex-col items-center">
            <div class="w-1.5 h-1.5 rounded-full bg-primary-container/20 group-hover:bg-primary group-hover:scale-150 transition-all border border-primary/40 relative z-10">
               <div class="absolute inset-0 bg-primary/40 blur-[4px] opacity-0 group-hover:opacity-100 transition-all"></div>
            </div>
            <div *ngIf="i < getEvents().length - 1" class="w-px flex-1 bg-primary/10 my-1 group-hover:bg-primary/30"></div>
          </div>
          <div class="pb-6 w-full translate-y-[-2px]">
            <div class="text-[0.55rem] text-primary/40 font-mono uppercase tracking-tighter mb-1 flex justify-between">
                <span>{{ event.date || 'Sequence_' + (i+1) }}</span>
                <span class="bg-primary/10 px-1 text-[0.45rem] tracking-widest opacity-0 group-hover:opacity-100 transition-all">DECIPHERED</span>
            </div>
            <p class="font-body text-xs text-on-surface/80 group-hover:text-on-surface transition-colors leading-relaxed italic pr-4">
              {{ event.event || event }}
            </p>
          </div>
        </div>
      </section>

      <!-- Future Predictions -->
      <section *ngIf="getPredictions().length > 0">
        <h3 class="text-[0.6rem] font-mono text-on-surface uppercase tracking-[0.3em] mb-4 border-b border-primary/10 pb-2 italic text-on-surface/60">Strategic Forecast</h3>
        <div class="grid grid-cols-1 gap-4">
           <div *ngFor="let pred of getPredictions(); let i = index" 
                class="p-4 bg-primary/5 hover:bg-primary/10 border-l border-primary/40 flex items-start gap-4 hover:border-primary transition-all group cursor-default">
              <span class="text-[0.55rem] font-mono text-primary/40 group-hover:text-primary">FORECAST_0{{ i+1 }}</span>
              <p class="text-[0.65rem] text-on-surface italic leading-snug">{{ pred }}</p>
           </div>
        </div>
      </section>
    </div>

    <!-- State Messages -->
    <div *ngIf="!timeline" class="h-64 flex flex-col items-center justify-center p-8 text-center gap-4">
        <div class="w-2 h-2 rounded-full bg-primary/20 animate-ping"></div>
        <span class="text-[0.6rem] font-mono text-primary/40 uppercase tracking-widest italic animate-pulse">Arc initialization pending...</span>
    </div>

    <div *ngIf="timeline?.loading" class="flex flex-col items-center py-12 gap-4">
      <div class="w-[200px] h-px bg-primary/10 relative overflow-hidden">
        <div class="absolute inset-0 bg-primary/60 animate-[shimmer_2s_infinite]"></div>
      </div>
      <span class="text-[0.6rem] font-mono text-primary/30 uppercase tracking-widest italic animate-pulse">Syncing Narrative Tensors...</span>
    </div>

    <div *ngIf="timeline?.error" class="text-error-container text-[0.55rem] font-mono p-4 uppercase border border-error-container/30 italic m-4">
      ERR: ARC_TRACER_TIMEOUT // {{ timeline.error }}
    </div>
  `,
  styles: [`:host { display: block; }`]
})
export class StoryArcComponent {
  @Input() timeline: any;
  errorMessage = "Market data currently unavailable for this ticker";

  getEvents(): any[] {
    if (!this.timeline) return [];
    if (this.timeline.loading) return [];
    
    // Explicitly set loading to false if we have data or error (handled by input usually, but reinforcing here)
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