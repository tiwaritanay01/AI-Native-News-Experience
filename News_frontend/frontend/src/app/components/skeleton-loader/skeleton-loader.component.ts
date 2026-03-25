import { Component } from '@angular/core';

@Component({
  selector:'app-skeleton-loader',
  standalone:true,
  template:`
  <div class="skeleton"></div>
  `,
  styles:[`
  .skeleton{
    height:100px;
    background:#eee;
    margin:10px 0;
  }
  `]
})
export class SkeletonLoaderComponent{}