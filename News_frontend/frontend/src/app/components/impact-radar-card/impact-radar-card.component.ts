import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-impact-radar-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="impact && !impact.loading && !impact.error" class="flex flex-col h-full">
      <div class="relative w-full aspect-square max-w-[280px] mx-auto mb-6">
        <!-- Dynamic Radar SVG -->
        <svg class="w-full h-full rotate-[-90deg]" viewBox="0 0 100 100">
          <circle class="stroke-primary-container/10 fill-none" cx="50" cy="50" r="45" stroke-width="0.5"></circle>
          <circle class="stroke-primary-container/10 fill-none" cx="50" cy="50" r="30" stroke-width="0.5"></circle>
          <circle class="stroke-primary-container/10 fill-none" cx="50" cy="50" r="15" stroke-width="0.5"></circle>
          <line class="stroke-primary-container/10" stroke-width="0.5" x1="50" x2="50" y1="5" y2="95"></line>
          <line class="stroke-primary-container/10" stroke-width="0.5" x1="5" x2="95" y1="50" y2="50"></line>
          <!-- Radar Sweep -->
          <path class="fill-secondary-container/20" d="M50 50 L50 5 A45 45 0 0 1 95 50 Z">
            <animateTransform attributeName="transform" dur="4s" from="0 50 50" repeatCount="indefinite" to="360 50 50" type="rotate"></animateTransform>
          </path>
          <!-- Data Points -->
          <circle class="fill-secondary-container animate-pulse" cx="70" cy="30" r="1.5"></circle>
          <circle class="fill-tertiary-container animate-pulse" cx="40" cy="75" r="1.2" style="animation-delay: 1s;"></circle>
          <circle class="fill-primary-container animate-pulse" cx="25" cy="40" r="1.8" style="animation-delay: 2s;"></circle>
        </svg>
        
        <!-- Radar Legend -->
        <div class="absolute inset-0 flex flex-col justify-between py-2 text-[0.5rem] font-mono text-primary-container/40 pointer-events-none">
          <div class="text-center uppercase tracking-widest">Global Market</div>
          <div class="flex justify-between px-2 uppercase tracking-widest">
            <span>Bearish</span>
            <span>Bullish</span>
          </div>
          <div class="text-center uppercase tracking-widest">Retail Interest</div>
        </div>
      </div>

      <div class="mt-auto">
        <div class="text-[0.625rem] text-primary-container/60 font-mono uppercase tracking-[0.1em] mb-3">Impact Analysis</div>
        <p class="font-body text-xs text-on-surface leading-normal italic opacity-80">
          {{ getImpactText() }}
        </p>
      </div>
    </div>

    <div *ngIf="impact?.loading" class="flex items-center justify-center h-full">
      <div class="w-16 h-16 border-2 border-primary-container/20 border-t-primary-container animate-spin rounded-full"></div>
    </div>

    <div *ngIf="impact?.error" class="text-tertiary-container text-[0.65rem] font-mono p-4 uppercase border border-tertiary-container/30">
      ERR: RADAR_SIGNAL_LOST // {{ impact.error }}
    </div>
  `,
  styles: [`:host { display: block; height: 100%; }`]
})
export class ImpactRadarCardComponent {
  @Input() impact: any;

  getImpactText(): string {
    if (!this.impact) return '';
    if (typeof this.impact === 'string') return this.impact;
    if (this.impact.impact) {
      if (typeof this.impact.impact === 'string') return this.impact.impact;
      if (this.impact.impact.raw) return this.impact.impact.raw;
    }
    if (this.impact.summary) return this.impact.summary;
    return 'Analysis successful. Signals normalized.';
  }
}