import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector:'app-contrarian-card',
  standalone:true,
  imports:[CommonModule],
  template:`
  <div *ngIf="opinions && !opinions.loading && !opinions.error">
    <h3 class="text-sm font-bold uppercase tracking-widest text-orange-400 mb-4">Contrarian Opinions</h3>

    <!-- Handle array of opinions -->
    <div *ngIf="isArray(opinions)" class="space-y-2">
      <div *ngFor="let opinion of opinions" class="flex gap-3 p-3 rounded-lg bg-slate-700/30">
        <div class="flex-shrink-0 rounded-full bg-orange-500 mt-2" style="width: 8px; height: 8px;"></div>
        <p class="text-xs text-slate-300">{{ opinion }}</p>
      </div>
    </div>

    <!-- Handle string response -->
    <div *ngIf="isString(opinions)" class="p-3 rounded-lg bg-slate-700/30">
      <p class="text-xs text-slate-300 whitespace-pre-wrap">{{ opinions }}</p>
    </div>

    <!-- Handle object response -->
    <div *ngIf="!isArray(opinions) && !isString(opinions)" class="space-y-2">
      <div class="p-3 rounded-lg bg-slate-700/30">
        <p class="text-xs text-slate-300 whitespace-pre-wrap">{{ getOpinionText() }}</p>
      </div>
    </div>
  </div>

  <div *ngIf="opinions?.loading" class="flex items-center justify-center h-full">
    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-orange-500"></div>
    <span class="text-xs text-slate-500 ml-2">Computing sentiment...</span>
  </div>

  <div *ngIf="opinions?.error" class="text-rose-400 text-sm">
    ⚠️ {{ opinions.error }}
  </div>
  `
})
export class ContrarianCardComponent {
  @Input() opinions: any;

  isArray(val: any): boolean {
    return Array.isArray(val);
  }

  isString(val: any): boolean {
    return typeof val === 'string';
  }

  getOpinionText(): string {
    if (!this.opinions) return '';
    if (this.opinions.contrarian_views) return this.opinions.contrarian_views;
    if (this.opinions.opinions) {
      if (typeof this.opinions.opinions === 'string') return this.opinions.opinions;
      if (Array.isArray(this.opinions.opinions)) return this.opinions.opinions.join('\n');
    }
    if (this.opinions.raw) return this.opinions.raw;
    if (this.opinions.summary) return this.opinions.summary;
    // Fallback: stringify the data
    const { loading, error, ...data } = this.opinions;
    return JSON.stringify(data, null, 2);
  }
}