import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-why-matters-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="relative h-full flex flex-col">
      <div class="flex-1 overflow-y-auto no-scrollbar pr-2 min-h-[120px]">
        <p class="font-body text-xl text-primary-container/80 leading-relaxed whitespace-pre-wrap">
          {{ getDisplayText() }}<span *ngIf="isGenerating" class="inline-block w-4 h-5 bg-secondary-container ml-1 animate-pulse align-middle"></span>
        </p>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; }
  `]
})
export class WhyMattersCardComponent {
  @Input() relevance: any;
  @Input() isGenerating: boolean = false;

  getDisplayText(): string {
    if (!this.relevance) {
      return this.isGenerating ? 'Initializing Intelligent Briefing...' : 'Awaiting narrative cluster...';
    }
    if (typeof this.relevance === 'string') {
      return this.relevance || (this.isGenerating ? 'Decoding TPU stream...' : 'Awaiting narrative cluster...');
    }
    if (this.relevance.summary) return this.relevance.summary;
    return this.isGenerating ? 'Processing JAX core...' : 'Decoding stream...';
  }
}
