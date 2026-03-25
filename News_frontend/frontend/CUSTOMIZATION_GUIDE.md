# AI-Native News Dashboard - Customization & Integration Guide

## Quick Customization Examples

### 1. Change Color Scheme

**Change Accent Color from Blue to Purple**

Find-and-replace in components:
```bash
# Before
text-blue-400 → text-purple-400
bg-blue-600 → bg-purple-600
border-blue-500 → border-purple-500
from-blue → from-purple
via-blue → via-purple

# Apply globally in hero-card.component.ts:
text-blue-400 tracking-widest
↓
text-purple-400 tracking-widest
```

### 2. Add Custom Company Watchlist

```typescript
// In dashboard-state.service.ts
export class DashboardStateService {
  private userWatchlistSignal = signal<string[]>(['AAPL', 'GOOGL', 'MSFT']);
  userWatchlist = this.userWatchlistSignal.asReadonly();

  addToWatchlist(ticker: string) {
    this.userWatchlistSignal.update(list => [...list, ticker]);
  }

  removeFromWatchlist(ticker: string) {
    this.userWatchlistSignal.update(list => 
      list.filter(t => t !== ticker)
    );
  }
}

// Use in impact-radar-card.component.ts:
@Component({
  template: `
    @for (company of getWatchedCompanies(); track company.ticker) {
      <div class="...">{{ company.ticker }}</div>
    }
  `
})
export class ImpactRadarCardComponent {
  getWatchedCompanies(): AffectedCompany[] {
    const watched = this.stateService.userWatchlist();
    return this.story().affectedCompanies.filter(
      c => watched.includes(c.ticker)
    );
  }
}
```

### 3. Add Real API Integration

```typescript
// In news.service.ts
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class NewsService {
  constructor(private http: HttpClient) {}

  getTopStory(): Observable<NewsStory> {
    return this.http.get<NewsStory>('/api/news/top');
  }

  getAllStories(filters?: NewsFilter): Observable<NewsStory[]> {
    let params = new HttpParams();
    if (filters?.sector) {
      params = params.set('sector', filters.sector);
    }
    return this.http.get<NewsStory[]>('/api/news', { params });
  }
}

// Update DashboardStateService to handle async
initializeDashboard() {
  this.loadingSignal.set(true);
  this.newsService.getTopStory().subscribe(
    (story) => {
      this.topStorySignal.set(story);
      this.loadingSignal.set(false);
    },
    (error) => {
      console.error('Failed to load top story', error);
      this.loadingSignal.set(false);
    }
  );
}
```

### 4. Replace Skeleton Loader with Real Loading State

```typescript
// In any card component
@Component({
  template: `
    @if (stateService.loading()) {
      <div class="space-y-3">
        <div class="h-4 bg-slate-700 rounded animate-pulse"></div>
        <div class="h-4 bg-slate-700 rounded animate-pulse w-5/6"></div>
      </div>
    } @else if (story(); as topStory) {
      <!-- Real content -->
    }
  `
})
export class HeroCardComponent {
  stateService = inject(DashboardStateService);
  story = input.required<NewsStory | null>();
}
```

### 5. Add Chart.js Integration

**Installation**
```bash
npm install chart.js ng2-charts rxjs
```

**Create Chart Component**
```typescript
// impact-radar-chart.component.ts
import { Component, input, ViewChild } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-impact-radar-chart',
  standalone: true,
  imports: [BaseChartDirective],
  template: `
    <div class="w-full h-48">
      <canvas baseChart
        [type]="'radar'"
        [data]="chartData"
        [options]="chartOptions">
      </canvas>
    </div>
  `
})
export class ImpactRadarChartComponent {
  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;
  
  story = input.required<NewsStory | null>();

  chartData = {
    labels: ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer'],
    datasets: [{
      label: 'Impact Score',
      data: [65, 45, 80, 55, 70],
      borderColor: '#3B82F6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      pointBackgroundColor: '#3B82F6',
      pointBorderColor: '#fff'
    }]
  };

  chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: '#fff' }
      }
    },
    scales: {
      r: {
        ticks: { color: '#cbd5e1' },
        grid: { color: '#475569' }
      }
    }
  };
}

// Update impact-radar-card.component.ts
import { ImpactRadarChartComponent } from './impact-radar-chart.component';

@Component({
  imports: [CommonModule, SkeletonLoaderComponent, ImpactRadarChartComponent],
  template: `
    <!-- Replace placeholder with -->
    <app-impact-radar-chart [story]="story()"></app-impact-radar-chart>
  `
})
export class ImpactRadarCardComponent { }
```

### 6. Implement Real-time Updates with WebSocket

```typescript
// realtime.service.ts
import { Injectable } from '@angular/core';
import { signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class RealtimeService {
  private priceUpdates = signal<Map<string, number>>(new Map());
  
  priceUpdates$ = this.priceUpdates.asReadonly();

  constructor() {
    this.connectWebSocket();
  }

  private connectWebSocket() {
    const ws = new WebSocket('wss://api.example.com/prices');
    
    ws.onmessage = (event) => {
      const { ticker, price } = JSON.parse(event.data);
      this.priceUpdates.update(prices => {
        const updated = new Map(prices);
        updated.set(ticker, price);
        return updated;
      });
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      // Reconnect after 5 seconds
      setTimeout(() => this.connectWebSocket(), 5000);
    };
  }

  getPriceChange(ticker: string, oldPrice: number): number {
    const newPrice = this.priceUpdates().get(ticker);
    if (!newPrice) return 0;
    return ((newPrice - oldPrice) / oldPrice) * 100;
  }
}

// Use in impact-radar-card.component.ts
@Component({
  template: `
    @for (company of affectedCompanies; track company.ticker) {
      @let priceChange = realtimeService.getPriceChange(
        company.ticker, 
        company.change
      );
      <div>
        <span>{{ company.ticker }}</span>
        <span [class.text-emerald-400]="priceChange > 0">
          {{ priceChange > 0 ? '+' : '' }}{{ priceChange }}%
        </span>
      </div>
    }
  `
})
export class ImpactRadarCardComponent {
  realtimeService = inject(RealtimeService);
  affectedCompanies = input<AffectedCompany[]>([]);
}
```

### 7. Add Story Search & Filter

```typescript
// search.service.ts
import { Injectable } from '@angular/core';
import { signal, computed } from '@angular/core';
import { NewsService } from './news.service';
import { NewsStory } from '../models/news.model';

@Injectable({ providedIn: 'root' })
export class SearchService {
  private searchQuerySignal = signal('');
  private filterImpactSignal = signal<'all' | 'bullish' | 'bearish' | 'neutral'>('all');
  
  searchQuery = this.searchQuerySignal.asReadonly();
  filterImpact = this.filterImpactSignal.asReadonly();

  filteredStories = computed(() => {
    const query = this.searchQuery().toLowerCase();
    const impact = this.filterImpact();
    const stories = this.newsService.getAllStories();

    return stories.filter(story => {
      const matchesQuery = 
        story.headline.toLowerCase().includes(query) ||
        story.summary.toLowerCase().includes(query);
      
      const matchesImpact = 
        impact === 'all' || story.impact === impact;

      return matchesQuery && matchesImpact;
    });
  });

  setSearchQuery(query: string) {
    this.searchQuerySignal.set(query);
  }

  setFilterImpact(impact: 'all' | 'bullish' | 'bearish' | 'neutral') {
    this.filterImpactSignal.set(impact);
  }
}

// Use in news-navigator.component.ts
@Component({
  template: `
    <div class="space-y-4">
      <input
        type="text"
        placeholder="Search news..."
        (input)="searchService.setSearchQuery($event.target.value)"
        class="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
      />
      
      <div class="flex gap-2">
        @for (impact of ['all', 'bullish', 'bearish', 'neutral']; track impact) {
          <button
            (click)="searchService.setFilterImpact(impact as any)"
            [class.bg-blue-600]="searchService.filterImpact() === impact"
            class="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-white">
            {{ impact | titlecase }}
          </button>
        }
      </div>

      <div class="space-y-3">
        @for (story of searchService.filteredStories(); track story.id) {
          <div class="bg-slate-800 p-4 rounded-lg border border-slate-700">
            <h3 class="font-semibold text-white">{{ story.headline }}</h3>
            <p class="text-sm text-slate-400 mt-2">{{ story.summary }}</p>
          </div>
        }
      </div>
    </div>
  `
})
export class NewsNavigatorComponent {
  searchService = inject(SearchService);
}
```

### 8. Add Responsive Mobile Menu

```typescript
// sidebar-navigation.component.ts
@Component({
  template: `
    <!-- Mobile menu button (only on mobile) -->
    <button 
      class="lg:hidden fixed top-4 left-4 z-50 p-2 bg-slate-800 rounded-lg"
      (click)="stateService.toggleSidebar()">
      ☰
    </button>

    <!-- Sidebar with overlay on mobile -->
    <div
      class="fixed lg:relative inset-y-0 left-0 z-40 lg:z-auto"
      [class.-translate-x-full]="!stateService.sidebarOpen() && isMobile()"
      [class.translate-x-0]="stateService.sidebarOpen() || !isMobile()"
      (click)="$event.stopPropagation()">
      <!-- Sidebar content -->
    </div>

    <!-- Mobile overlay -->
    <div
      *ngIf="stateService.sidebarOpen() && isMobile()"
      class="fixed inset-0 z-30 bg-black/50"
      (click)="stateService.setSidebarOpen(false)">
    </div>
  `
})
export class SidebarNavigationComponent {
  stateService = inject(DashboardStateService);
  
  isMobile(): boolean {
    return window.innerWidth < 1024;
  }
}
```

### 9. Add Dark/Light Theme Toggle

```typescript
// theme.service.ts
import { Injectable } from '@angular/core';
import { signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private themeSignal = signal<'dark' | 'light'>('dark');
  theme = this.themeSignal.asReadonly();

  constructor() {
    const saved = localStorage.getItem('theme');
    if (saved) {
      this.themeSignal.set(saved as 'dark' | 'light');
    }
  }

  toggleTheme() {
    this.themeSignal.update(t => t === 'dark' ? 'light' : 'dark');
    localStorage.setItem('theme', this.themeSignal());
    this.applyTheme();
  }

  private applyTheme() {
    const html = document.documentElement;
    html.classList.toggle('dark', this.themeSignal() === 'dark');
  }
}
```

### 10. Add User Preferences Storage

```typescript
// preferences.service.ts
import { Injectable } from '@angular/core';
import { signal } from '@angular/core';

interface UserPreferences {
  explainLevel: 'beginner' | 'intermediate' | 'expert';
  watchlist: string[];
  theme: 'dark' | 'light';
  sidebarCollapsed: boolean;
  newsCategories: string[];
}

@Injectable({ providedIn: 'root' })
export class PreferencesService {
  private preferencesSignal = signal<UserPreferences>(this.loadPreferences());

  preferences = this.preferencesSignal.asReadonly();

  savePreferences(prefs: Partial<UserPreferences>) {
    this.preferencesSignal.update(current => ({
      ...current,
      ...prefs
    }));
    localStorage.setItem(
      'preferences',
      JSON.stringify(this.preferencesSignal())
    );
  }

  private loadPreferences(): UserPreferences {
    const saved = localStorage.getItem('preferences');
    return saved ? JSON.parse(saved) : {
      explainLevel: 'intermediate',
      watchlist: [],
      theme: 'dark',
      sidebarCollapsed: false,
      newsCategories: ['Technology', 'Finance', 'Healthcare']
    };
  }
}
```

## Deployment Checklist

- [ ] Replace mock data with real API calls
- [ ] Add authentication/login flow
- [ ] Implement error handling and toast notifications
- [ ] Add analytics tracking
- [ ] Configure environment variables
- [ ] Run production build
- [ ] Test in production environment
- [ ] Set up CI/CD pipeline
- [ ] Monitor performance metrics
- [ ] Set up error logging (Sentry, etc.)

## Testing Examples

```bash
# Run unit tests
npm test

# Create test file for hero-card
ng generate component hero-card --skip-tests=false
```

```typescript
// hero-card.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HeroCardComponent } from './hero-card.component';
import { DashboardStateService } from '../../services/dashboard-state.service';

describe('HeroCardComponent', () => {
  let component: HeroCardComponent;
  let fixture: ComponentFixture<HeroCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeroCardComponent],
      providers: [DashboardStateService]
    }).compileComponents();

    fixture = TestBed.createComponent(HeroCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should display story headline', () => {
    const headline = fixture.nativeElement.querySelector('h3');
    expect(headline.textContent).toContain('');
  });

  it('should toggle explain level', () => {
    const buttons = fixture.nativeElement.querySelectorAll('button');
    buttons[0].click();
    expect(component.stateService.explainLevel()).toBe('beginner');
  });
});
```

---

These examples should help you extend the dashboard with real integrations and custom features!
