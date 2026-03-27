import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-contrarian-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="opinions && !opinions.loading && !opinions.error" class="space-y-6">
      <div class="border-l-2 border-secondary-container pl-4 py-1">
        <div class="text-[0.625rem] text-secondary-container font-mono uppercase tracking-[0.1em] mb-1 italic">Bullish Case / Synthesis</div>
        <p class="font-body text-sm text-on-surface line-clamp-3 italic">
          {{ getPerspective(0) }}
        </p>
      </div>
      <div class="border-l-2 border-tertiary-container pl-4 py-1">
        <div class="text-[0.625rem] text-tertiary-container font-mono uppercase tracking-[0.1em] mb-1 italic">Bearish Case / Risks</div>
        <p class="font-body text-sm text-on-surface line-clamp-3 italic opacity-80">
          {{ getPerspective(1) }}
        </p>
      </div>
      <div *ngIf="getPerspectiveCount() > 2" class="border-l-2 border-primary-container pl-4 py-1">
        <div class="text-[0.625rem] text-primary-container font-mono uppercase tracking-[0.1em] mb-1 italic">Contrarian Synthesis</div>
        <p class="font-body text-sm text-on-surface line-clamp-2 italic opacity-60">
          {{ getPerspective(2) }}
        </p>
      </div>
    </div>

    <div *ngIf="opinions?.loading" class="flex flex-col items-center justify-center h-full gap-4">
      <div class="w-12 h-1 bg-primary/20 relative overflow-hidden">
        <div class="absolute inset-0 bg-primary animate-[ticker_2s_linear_infinite]"></div>
      </div>
      <span class="text-[0.65rem] font-mono text-primary/40 uppercase tracking-widest">Computing Sentiment...</span>
    </div>

    <div *ngIf="opinions?.error" class="text-tertiary-container text-[0.65rem] font-mono uppercase border border-tertiary-container/30 p-4">
      ERR: LOG_ANALYSIS_FAILURE // {{ opinions.error }}
    </div>
  `,
  styles: [`
    @keyframes ticker {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }
  `]
})
export class ContrarianCardComponent {
  @Input() opinions: any;

  getPerspective(index: number): string {
    const list = this.getPerspectiveList();
    return list[index] || (index === 0 ? 'Synthesis in progress...' : 'Awaiting alternative viewpoints...');
  }

  getPerspectiveCount(): number {
    return this.getPerspectiveList().length;
  }

  private getPerspectiveList(): string[] {
    if (!this.opinions) return [];
    if (Array.isArray(this.opinions)) return this.opinions;
    if (this.opinions.opinions && Array.isArray(this.opinions.opinions)) return this.opinions.opinions;
    if (this.opinions.contrarian_views && Array.isArray(this.opinions.contrarian_views)) return this.opinions.contrarian_views;
    if (typeof this.opinions === 'string') return this.opinions.split('\n').filter(s => s.trim());
    return [];
  }
}