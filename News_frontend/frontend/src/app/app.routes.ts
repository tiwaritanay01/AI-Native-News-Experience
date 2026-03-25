import { Routes } from '@angular/router';
import { DashboardLayoutComponent } from './components/dashboard-layout/dashboard-layout.component';
import { StoryArcComponent } from './components/story-arc/story-arc.component';
import { NewsNavigatorComponent } from './components/news-navigator/news-navigator.component';
import { VideoStudioComponent } from './components/video-studio/video-studio.component';
import { VernacularComponent } from './components/vernacular/vernacular.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    component: DashboardLayoutComponent
  },
  {
    path: 'dashboard/:id',
    component: DashboardLayoutComponent
  },
  {
    path: 'story-arc',
    component: StoryArcComponent
  },
  {
    path: 'news-navigator',
    component: NewsNavigatorComponent
  },
  {
    path: 'video-studio',
    component: VideoStudioComponent
  },
  {
    path: 'vernacular',
    component: VernacularComponent
  }
];
