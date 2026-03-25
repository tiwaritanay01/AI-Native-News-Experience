// import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector:'app-impact-radar-card',
  standalone:true,
  imports:[CommonModule],
  template:`
  <div class="card" *ngIf="impact">
    <h3>Impact Radar</h3>

    <div *ngFor="let item of impact | keyvalue">
      <b>{{item.key}}</b> : {{item.value}}
    </div>

  </div>
  `
})
export class ImpactRadarCardComponent{

  @Input() impact:any;

}