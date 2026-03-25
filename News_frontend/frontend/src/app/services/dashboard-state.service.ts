import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { signal, computed } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { DashboardState, ExplainLevel, NewsStory } from '../models/news.model';
import { NewsService } from './news.service';

@Injectable({
  providedIn: 'root'
})
export class DashboardStateService {

  private explainLevelSignal = signal<ExplainLevel>('intermediate');
  private sidebarOpenSignal = signal(true);
  private loadingSignal = signal(false);
  private topStorySignal = signal<NewsStory | null>(null);
  private relatedNewsSignal = signal<NewsStory[]>([]);

  explainLevel = this.explainLevelSignal.asReadonly();
  sidebarOpen = this.sidebarOpenSignal.asReadonly();
  loading = this.loadingSignal.asReadonly();
  topStory = this.topStorySignal.asReadonly();
  relatedNews = this.relatedNewsSignal.asReadonly();

  dashboardState = computed<DashboardState>(() => ({
    topStory: this.topStory(),
    relatedNews: this.relatedNews(),
    explainLevel: this.explainLevel(),
    sidebarOpen: this.sidebarOpen(),
    loading: this.loading()
  }));

  constructor(
    private newsService: NewsService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {

    if (isPlatformBrowser(this.platformId)) {
      this.initializeDashboard();
    }

  }

  private initializeDashboard() {

    this.loadingSignal.set(true);

    this.newsService.getTopStory().subscribe((data:any)=>{
      this.topStorySignal.set(data);
    });

    this.newsService.getRelatedNews(2).subscribe((data:any)=>{
      this.relatedNewsSignal.set(data);
      this.loadingSignal.set(false);
    });

  }

  toggleExplainLevel() {
    const current = this.explainLevelSignal();
    const levels: ExplainLevel[] = ['beginner', 'intermediate', 'expert'];
    const nextIndex = (levels.indexOf(current) + 1) % levels.length;
    this.explainLevelSignal.set(levels[nextIndex]);
  }

  setExplainLevel(level: ExplainLevel) {
    this.explainLevelSignal.set(level);
  }

  toggleSidebar() {
    this.sidebarOpenSignal.update((val) => !val);
  }

  setSidebarOpen(open: boolean) {
    this.sidebarOpenSignal.set(open);
  }

  setTopStory(story: NewsStory) {
    this.topStorySignal.set(story);
  }

  setRelatedNews(news: NewsStory[]) {
    this.relatedNewsSignal.set(news);
  }
}