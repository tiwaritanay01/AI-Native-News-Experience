// import { Component, inject } from '@angular/core';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-story-arc',
//   standalone: true,
//   imports: [CommonModule],
//   template: `
//     <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8">
//       <!-- Header -->
//       <div class="mb-8">
//         <a href="/dashboard" class="text-blue-400 hover:text-blue-300 text-sm font-medium mb-4 inline-block">
//           ← Back to Dashboard
//         </a>
//         <h1 class="text-4xl font-bold text-white mb-2">Story Arc Visualization</h1>
//         <p class="text-slate-400">
//           Explore the interconnected network of companies, regulations, and market events
//         </p>
//       </div>

//       <!-- Network Graph Container -->
//       <div
//         class="w-full h-96 lg:h-screen bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl border border-slate-700 flex items-center justify-center overflow-hidden relative">
//         <!-- Placeholder for D3.js / React Flow network graph -->
//         <div class="text-center">
//           <div class="mb-6">
//             <svg class="w-24 h-24 mx-auto text-blue-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//               <path
//                 stroke-linecap="round"
//                 stroke-linejoin="round"
//                 stroke-width="2"
//                 d="M13 10V3L4 14h7v7l9-11h-7z"></path>
//             </svg>
//           </div>
//           <h3 class="text-xl font-semibold text-white mb-2">Interactive Network Graph</h3>
//           <p class="text-slate-400 mb-6 max-w-md">
//             D3.js / React Flow integration placeholder - Connect companies, regulations, and market events
//           </p>
//           <div class="flex gap-4 justify-center">
//             <button
//               class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-all duration-200 transform hover:scale-105 active:scale-95">
//               Load Sample Network
//             </button>
//             <button
//               class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-all duration-200">
//               Export as SVG
//             </button>
//           </div>
//         </div>

//         <!-- Animated background elements -->
//         <div class="absolute inset-0 pointer-events-none">
//           <div
//             class="absolute top-20 left-20 w-32 h-32 border-2 border-blue-500/20 rounded-full animate-pulse"></div>
//           <div
//             class="absolute bottom-20 right-20 w-40 h-40 border-2 border-emerald-500/10 rounded-full animate-pulse"
//             style="animation-delay: 0.5s;"></div>
//           <div
//             class="absolute top-1/2 left-1/2 w-48 h-48 border-2 border-violet-500/10 rounded-full animate-pulse"
//             style="animation-delay: 1s;"></div>
//         </div>
//       </div>

//       <!-- Legend / Info Section -->
//       <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
//         <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg p-6 border border-slate-700">
//           <div class="flex items-center gap-3 mb-3">
//             <div class="w-3 h-3 rounded-full bg-blue-500"></div>
//             <h4 class="font-semibold text-white">Companies</h4>
//           </div>
//           <p class="text-sm text-slate-400">
//             Market participants directly affected by news and events
//           </p>
//         </div>

//         <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg p-6 border border-slate-700">
//           <div class="flex items-center gap-3 mb-3">
//             <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
//             <h4 class="font-semibold text-white">Regulations</h4>
//           </div>
//           <p class="text-sm text-slate-400">
//             Policy changes and regulatory actions shaping the market
//           </p>
//         </div>

//         <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg p-6 border border-slate-700">
//           <div class="flex items-center gap-3 mb-3">
//             <div class="w-3 h-3 rounded-full bg-violet-500"></div>
//             <h4 class="font-semibold text-white">Events</h4>
//           </div>
//           <p class="text-sm text-slate-400">
//             Market catalysts and significant developments
//           </p>
//         </div>
//       </div>
//     </div>
//   `,
//   styles: []
// })
// export class StoryArcComponent {}
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector:'app-story-arc',
  standalone:true,
  imports:[CommonModule],
  template:`

  <div class="card">

    <h3>Story Timeline</h3>

    <ul>
      <li *ngFor="let event of timeline">
        {{event}}
      </li>
    </ul>

  </div>

  `
})
export class StoryArcComponent{

  @Input() timeline:any[]=[];

}