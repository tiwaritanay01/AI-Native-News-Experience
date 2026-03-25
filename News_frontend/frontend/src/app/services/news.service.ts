import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { of, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NewsService {

  // api = "http://localhost:8000";
  private api = 'https://hypernatural-phoebe-blowy.ngrok-free.dev';

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  private isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  getStories(): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/stories`);
  }

  getStoryOfDay(): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story-of-day`);
  }

  getDashboard(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/dashboard`);
  }

  getImpact(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/impact`);
  }

  getTimeline(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/timeline`);
  }

  getOpinions(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/opinions`);
  }

  getTopStory(): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story-of-day`);
  }

  getBriefing(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/briefing`);
  }

  getSentiment(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/sentiment`);
  }

  getQuestions(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/questions`);
  }

  getRelatedNews(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/stories`);
  }

}