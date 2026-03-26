import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector:'app-why-matters-card',
  standalone:true,
  imports:[CommonModule],
  template:`
  <div class="relative h-full flex flex-col">
    <div class="flex items-center gap-2 mb-4">
      <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
      <h3 class="text-xs font-bold uppercase tracking-widest text-emerald-400">Personalized Briefing</h3>
    </div>

    <div class="flex-1 overflow-y-auto custom-scrollbar pr-2">
      <p class="text-slate-100 text-sm leading-relaxed font-mono whitespace-pre-wrap">
        {{ getDisplayText() }}<span *ngIf="isGenerating" class="inline-block w-1.5 h-4 bg-emerald-500 ml-0.5 animate-pulse align-middle"></span>
      </p>
    </div>

    <div class="mt-4 pt-4 border-t border-slate-800/50 flex justify-between items-center">
       <span class="text-[10px] text-slate-500 font-mono">XLA/TPU_v5e-1</span>
       <span class="text-[10px] text-emerald-500/50 font-mono uppercase">Optimized Channel</span>
    </div>
  </div>
  `,
  styles: [`
    .custom-scrollbar::-webkit-scrollbar { width: 4px; }
    .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
    .custom-scrollbar::-webkit-scrollbar-thumb { 
      background: #1e293b; 
      border-radius: 10px; 
    }
  `]
})
export class WhyMattersCardComponent {
  @Input() relevance: any;
  @Input() isGenerating: boolean = false;

  getDisplayText(): string {
    if (!this.relevance) {
      return this.isGenerating ? 'Initializing JAX Engine...' : 'Waiting for TPU core...';
    }
    // Handle string directly (the streaming text)
    if (typeof this.relevance === 'string') {
      return this.relevance || (this.isGenerating ? 'Initializing JAX Engine...' : 'Waiting for TPU core...');
    }
    // Handle object with summary property
    if (this.relevance.summary) return this.relevance.summary;
    return this.isGenerating ? 'Initializing JAX Engine...' : 'Decoding stream...';
  }
}
