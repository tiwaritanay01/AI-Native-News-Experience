// import { Component } from '@angular/core';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-news-navigator',
//   standalone: true,
//   imports: [CommonModule],
//   template: `
//     <div class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8">
//       <a href="/dashboard" class="text-blue-400 hover:text-blue-300 text-sm font-medium mb-4 inline-block">
//         ← Back to Dashboard
//       </a>
//       <div class="max-w-2xl">
//         <h1 class="text-4xl font-bold text-white mb-4">News Navigator</h1>
//         <p class="text-slate-400 mb-8">
//           Explore news by category, ticker, or custom filters
//         </p>
//         <div class="bg-slate-800 rounded-lg p-8 border border-slate-700 text-center">
//           <svg class="w-16 h-16 mx-auto text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
//           </svg>
//           <h3 class="text-white font-semibold mb-2">Coming Soon</h3>
//           <p class="text-slate-400">Advanced news filtering and discovery tools</p>
//         </div>
//       </div>
//     </div>
//   `
// })
// export class NewsNavigatorComponent {}
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-news-navigator',
  standalone: true,
  imports: [CommonModule],
  template: `
  <div class="news-feed">
    <h2>News Navigator</h2>

    <div *ngFor="let story of stories" class="story-card" (click)="openStory(story.cluster_id)">
      <h3>{{story.title}}</h3>
      <p>{{story.summary}}</p>
    </div>
  </div>
  `,
  styles:[`
  .story-card{
    border:1px solid #ddd;
    padding:15px;
    margin:10px;
    cursor:pointer;
  }
  `]
})
export class NewsNavigatorComponent implements OnInit {

  stories:any[]=[];

  constructor(private news:NewsService, private router:Router){}

  ngOnInit(){
    this.news.getStories().subscribe((data:any)=>{
      this.stories=data;
    });
  }

  openStory(id:number){
    this.router.navigate(['/dashboard', id]);
  }
}