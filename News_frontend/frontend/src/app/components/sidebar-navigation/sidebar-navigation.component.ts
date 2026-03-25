// import { Component, inject } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { Router } from '@angular/router';
// import { DashboardStateService } from '../../services/dashboard-state.service';

// @Component({
//   selector: 'app-sidebar-navigation',
//   standalone: true,
//   imports: [CommonModule],
//   template: `
//     <div
//       class="h-screen bg-gradient-to-b from-slate-900 to-slate-950 border-r border-slate-700 transition-all duration-300 flex flex-col"
//       [class.w-64]="stateService.sidebarOpen()"
//       [class.w-20]="!stateService.sidebarOpen()">
//       <!-- Logo Section -->
//       <div
//         class="flex items-center justify-between p-4 border-b border-slate-700"
//         [class.justify-center]="!stateService.sidebarOpen()">
//         <div class="flex items-center gap-3" [class.hidden]="!stateService.sidebarOpen()">
//           <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
//             <span class="text-white font-bold text-sm">AI</span>
//           </div>
//           <span class="text-lg font-bold text-white">NewsHub</span>
//         </div>
//         <button
//           (click)="stateService.toggleSidebar()"
//           class="p-2 rounded-lg hover:bg-slate-800 transition-all duration-200 text-slate-400 hover:text-white">
//           <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path
//               stroke-linecap="round"
//               stroke-linejoin="round"
//               stroke-width="2"
//               d="M4 6h16M4 12h16M4 18h16"></path>
//           </svg>
//         </button>
//       </div>

//       <!-- Navigation Items -->
//       <nav class="flex-1 p-4 space-y-2">
//         @for (item of navItems; track item.id) {
//           <button
//             (click)="navigate(item.route)"
//             class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 transition-all duration-200 group"
//             [class.bg-slate-800]="isActive(item.route)"
//             [class.text-blue-400]="isActive(item.route)">
//             <span class="flex-shrink-0 inline-block">
//               {{ item.icon }}
//             </span>
//             <span
//               class="text-sm font-medium truncate"
//               [class.hidden]="!stateService.sidebarOpen()">
//               {{ item.label }}
//             </span>
//           </button>
//         }
//       </nav>

//       <!-- Footer -->
//       <div class="p-4 border-t border-slate-700">
//         <button
//           class="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition-all duration-200"
//           [class.justify-center]="!stateService.sidebarOpen()">
//           <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path
//               stroke-linecap="round"
//               stroke-linejoin="round"
//               stroke-width="2"
//               d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
//           </svg>
//           <span class="text-sm font-medium" [class.hidden]="!stateService.sidebarOpen()">
//             Sign Out
//           </span>
//         </button>
//       </div>
//     </div>
//   `,
//   styles: []
// })
// export class SidebarNavigationComponent {
//   stateService = inject(DashboardStateService);
//   router = inject(Router);

//   navItems = [
//     { id: 'personalized', label: 'My ET', route: '/dashboard', icon: '⚡' },
//     { id: 'news-navigator', label: 'News Navigator', route: '/news-navigator', icon: '🧭' },
//     { id: 'story-arc', label: 'Story Arc', route: '/story-arc', icon: '🔗' },
//     { id: 'video-studio', label: 'Video Studio', route: '/video-studio', icon: '▶️' },
//     { id: 'vernacular', label: 'Vernacular', route: '/vernacular', icon: '🌐' }
//   ];

//   navigate(route: string) {
//     this.router.navigate([route]);
//   }

//   isActive(route: string): boolean {
//     return this.router.url === route;
//   }
// }
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector:'app-sidebar-navigation',
  standalone:true,
  imports:[CommonModule,RouterModule],
  template:`

  <div class="sidebar">

    <a routerLink="/">Home</a>
    <a routerLink="/navigator">News Navigator</a>
    <a routerLink="/video">Video Studio</a>
    <a routerLink="/vernacular">Vernacular</a>

  </div>

  `
})
export class SidebarNavigationComponent{}