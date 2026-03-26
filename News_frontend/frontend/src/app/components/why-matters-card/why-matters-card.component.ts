// import { Component, input, inject } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { NewsStory } from '../../models/news.model';
// import { SkeletonLoaderComponent } from '../skeleton-loader/skeleton-loader.component';
// import { DashboardStateService } from '../../services/dashboard-state.service';

// @Component({
//   selector: 'app-why-matters-card',
//   standalone: true,
//   imports: [CommonModule, SkeletonLoaderComponent],
//   template: `
//     <div
//       class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 overflow-hidden group hover:border-emerald-500/50 transition-all duration-300">
//       <!-- Hover glow -->
//       <div
//         class="absolute -inset-1 bg-gradient-to-r from-emerald-600 via-emerald-500 to-cyan-500 opacity-0 group-hover:opacity-20 blur-xl transition-all duration-500 -z-10">
//       </div>

//       <div class="relative z-10 space-y-4">
//         <div>
//           <h3 class="text-sm font-semibold text-emerald-400 tracking-widest uppercase mb-4">
//             Why This Matters To You
//           </h3>
//         </div>

//         @if (stateService.loading()) {
//           <app-skeleton-loader [lines]="3"></app-skeleton-loader>
//         } @else if (story(); as topStory) {
//           <div class="space-y-3">
//             @for (i of [0, 1, 2]; track i) {
//               <div class="flex gap-3 p-3 rounded-lg bg-slate-700/30 hover:bg-slate-700/50 transition-all duration-200">
//                 <div class="flex-shrink-0 rounded-full bg-emerald-500 mt-2" style="width: 8px; height: 8px;"></div>
//                 <div class="flex-1">
//                   <p class="text-sm text-slate-100">
//                     {{ getRelevantPoint(topStory, i) }}
//                   </p>
//                 </div>
//               </div>
//             }
//           </div>
//         }
//       </div>
//     </div>
//   `
// })
// export class WhyMattersCardComponent {
//   stateService = inject(DashboardStateService);
//   story = input.required<NewsStory | null>();

//   getRelevantPoint(story: NewsStory, index: number): string {
//     const points = [
//       `${story.affectedCompanies[0]?.name || 'Key companies'} directly impacted by this news`,
//       `Your portfolio alignment: ${story.impact === 'bullish' ? 'Positive exposure' : story.impact === 'bearish' ? 'Risk exposure' : 'Neutral position'}`,
//       `Sector impact on ${story.affectedCompanies[0]?.sector || 'Technology'}: Monitor for follow-up developments`
//     ];
//     return points[index];
//   }
// }
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
        {{ getDisplayBriefing() }}<span *ngIf="isGenerating" class="w-1.5 h-4 inline-block bg-emerald-500 ml-1 animate-pulse"></span>
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

  getDisplayBriefing(): string {
    if (!this.relevance) return 'Waiting for TPU core...';
    if (typeof this.relevance === 'string') return this.relevance;
    return this.relevance.summary || 'Decoding stream...';
  }
}
