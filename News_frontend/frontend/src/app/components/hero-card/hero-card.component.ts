// import { Component, inject, input } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { DashboardStateService } from '../../services/dashboard-state.service';
// import { NewsStory, ExplainLevel } from '../../models/news.model';
// import { SkeletonLoaderComponent } from '../skeleton-loader/skeleton-loader.component';

// @Component({
//   selector: 'app-hero-card',
//   standalone: true,
//   imports: [CommonModule, SkeletonLoaderComponent],
//   template: `
//     <div
//       class="relative col-span-1 lg:col-span-2 bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 overflow-hidden group hover:border-blue-500/50 transition-all duration-300">
//       <!-- Glassmorphism background effect -->
//       <div
//         class="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-blue-500/5 to-blue-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
//       </div>

//       <!-- Glow effect on hover -->
//       <div
//         class="absolute -inset-1 bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 opacity-0 group-hover:opacity-20 blur-xl transition-all duration-500 -z-10">
//       </div>

//       <div class="relative z-10 space-y-6">
//         <!-- Header with explain level toggle -->
//         <div class="flex justify-between items-start">
//           <div>
//             <h2 class="text-sm font-semibold text-blue-400 tracking-widest uppercase">
//               The Interactive Briefing
//             </h2>
//           </div>

//           <!-- Explain Level Toggle -->
//           <div class="flex gap-2">
//             <button
//               *ngFor="let level of explainLevels"
//               (click)="setExplainLevel(level)"
//               [class.bg-blue-600]="stateService.explainLevel() === level"
//               [class.text-white]="stateService.explainLevel() === level"
//               [class.bg-slate-700]="stateService.explainLevel() !== level"
//               [class.text-slate-300]="stateService.explainLevel() !== level"
//               class="px-3 py-1 rounded text-xs font-medium transition-all duration-200 hover:scale-105">
//               {{ formatLevel(level) }}
//             </button>
//           </div>
//         </div>

//         @if (stateService.loading()) {
//           <app-skeleton-loader [lines]="4"></app-skeleton-loader>
//         } @else if (story(); as topStory) {
//           <!-- Story Headline -->
//           <div>
//             <h3 class="text-2xl font-bold text-white leading-tight mb-2">
//               {{ topStory.headline }}
//             </h3>
//             <p class="text-sm text-slate-400">{{ topStory.summary }}</p>
//           </div>

//           <!-- Bullet Points -->
//           <div class="space-y-2">
//             @for (bullet of topStory.bulletPoints; track $index) {
//               <div class="flex gap-3">
//                 <div class="flex-shrink-0 text-blue-400 font-bold">•</div>
//                 <p class="text-sm text-slate-300">{{ bullet }}</p>
//               </div>
//             }
//           </div>

//           <!-- Chat Input -->
//           <div class="pt-4 border-t border-slate-700">
//             <div class="flex gap-2">
//               <input
//                 type="text"
//                 placeholder="Ask AI about this story..."
//                 class="flex-1 bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-200" />
//               <button
//                 class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 active:scale-95">
//                 Ask
//               </button>
//             </div>
//           </div>
//         }
//       </div>
//     </div>
//   `,
//   styles: []
// })
// export class HeroCardComponent {
//   stateService = inject(DashboardStateService);
//   story = input.required<NewsStory | null>();

//   explainLevels: ExplainLevel[] = ['beginner', 'intermediate', 'expert'];

//   setExplainLevel(level: ExplainLevel) {
//     this.stateService.setExplainLevel(level);
//   }

//   formatLevel(level: ExplainLevel): string {
//     return level.charAt(0).toUpperCase() + level.slice(1);
//   }
// }
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';

@Component({
  selector:'app-hero-card',
  standalone:true,
  imports:[CommonModule],
  template:`
  <div class="hero" *ngIf="story">
    <h2>Story of the Day</h2>
    <h3>{{story.title}}</h3>
    <p>{{story.summary}}</p>
  </div>
  `
})
export class HeroCardComponent implements OnInit{

  story:any;

  constructor(private news:NewsService){}

  ngOnInit(){
    this.news.getStoryOfDay().subscribe((data:any)=>{
      this.story=data;
    });
  }

}