import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { of, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NewsService {

  public api = 'https://hypernatural-phoebe-blowy.ngrok-free.dev';
  
  public headers = new HttpHeaders({
    'ngrok-skip-browser-warning': 'true'
  });

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  private isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  getStories(): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/stories`, { headers: this.headers });
  }

  getStoryOfDay(): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story-of-day`, { headers: this.headers });
  }

  getDashboard(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/dashboard`, { headers: this.headers });
  }

  getImpact(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/impact`, { headers: this.headers });
  }

  getTimeline(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/timeline`, { headers: this.headers });
  }

  getOpinions(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/opinions`, { headers: this.headers });
  }

  getTopStory(): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story-of-day`, { headers: this.headers });
  }

  getBriefing(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/briefing`, { headers: this.headers });
  }

  getSentiment(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/sentiment`, { headers: this.headers });
  }

  getQuestions(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/story/${clusterId}/questions`, { headers: this.headers });
  }

  getRelatedNews(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/stories`, { headers: this.headers });
  }

  getStoryVideo(clusterId: number): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.post<any>(`${this.api}/api/story/${clusterId}/video`, {}, { headers: this.headers });
  }

  getStoryTranslation(clusterId: number, lang: string): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/api/story/${clusterId}/translate?lang=${lang}`, { headers: this.headers });
  }

  getMarketTicker(): Observable<any> {
    if (!this.isBrowser()) return of(null);
    return this.http.get<any>(`${this.api}/api/market/ticker`, { headers: this.headers });
  }

}