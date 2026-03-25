// import { Component, input, inject } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { NewsStory } from '../../models/news.model';
// import { SkeletonLoaderComponent } from '../skeleton-loader/skeleton-loader.component';
// import { DashboardStateService } from '../../services/dashboard-state.service';

// @Component({
//   selector: 'app-contrarian-card',
//   standalone: true,
//   imports: [CommonModule, SkeletonLoaderComponent],
//   template: `
//     <div
//       class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 overflow-hidden group hover:border-violet-500/50 transition-all duration-300">
//       <!-- Hover glow -->
//       <div
//         class="absolute -inset-1 bg-gradient-to-r from-violet-600 via-violet-500 to-purple-500 opacity-0 group-hover:opacity-20 blur-xl transition-all duration-500 -z-10">
//       </div>

//       <div class="relative z-10 space-y-4">
//         <h3 class="text-sm font-semibold text-violet-400 tracking-widest uppercase">
//           Contrarian Perspective
//         </h3>

//         @if (stateService.loading()) {
//           <app-skeleton-loader [lines]="4"></app-skeleton-loader>
//         } @else if (story(); as topStory) {
//           <div class="grid grid-cols-2 gap-4 h-full">
//             <!-- Bullish View -->
//             <div
//               class="bg-gradient-to-br from-emerald-900/30 to-emerald-800/20 border border-emerald-700/50 rounded-lg p-4 hover:border-emerald-500/50 transition-all duration-200">
//               <div class="flex items-center gap-2 mb-3">
//                 <div class="rounded-full bg-emerald-500" style="width: 8px; height: 8px;"></div>
//                 <h4 class="text-sm font-semibold text-emerald-400 uppercase tracking-wide">Bullish</h4>
//               </div>
//               <p class="text-xs text-slate-300 leading-relaxed">{{ topStory.bullishView }}</p>
//             </div>

//             <!-- Bearish View -->
//             <div
//               class="bg-gradient-to-br from-rose-900/30 to-rose-800/20 border border-rose-700/50 rounded-lg p-4 hover:border-rose-500/50 transition-all duration-200">
//               <div class="flex items-center gap-2 mb-3">
//                 <div class="rounded-full bg-rose-500" style="width: 8px; height: 8px;"></div>
//                 <h4 class="text-sm font-semibold text-rose-400 uppercase tracking-wide">Bearish</h4>
//               </div>
//               <p class="text-xs text-slate-300 leading-relaxed">{{ topStory.bearishView }}</p>
//             </div>
//           </div>
//         }
//       </div>
//     </div>
//   `
// })
// export class ContrarianceCardComponent {
//   stateService = inject(DashboardStateService);
//   story = input.required<NewsStory | null>();
// }
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector:'app-contrarian-card',
  standalone:true,
  imports:[CommonModule],
  template:`

  <div class="card">

    <h3>Contrarian Opinions</h3>

    <div *ngFor="let opinion of opinions">
      <p>{{opinion}}</p>
    </div>

  </div>

  `
})
export class ContrarianCardComponent{

  @Input() opinions:any[]=[];

}