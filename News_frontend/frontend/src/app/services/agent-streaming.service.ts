import { Injectable, NgZone, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AgentStreamingService {

  private apiBase = 'https://hypernatural-phoebe-blowy.ngrok-free.dev';

  constructor(
    private zone: NgZone,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  /**
   * Consumes an SSE stream from the FastAPI backend using the Web Fetch API 
   * and ReadableStream. This supports POST requests, unlike the standard EventSource.
   * 
   * @param clusterId The ID of the news cluster to analyze.
   * @param prompt User-defined or automated prompt for the AI agent.
   * @returns Observable that emits text chunks in real-time.
   */
  streamAgentResponse(clusterId: number, prompt: string = 'Latest news briefing'): Observable<string> {
    
    return new Observable<string>(observer => {
      
      if (!isPlatformBrowser(this.platformId)) {
        observer.complete();
        return;
      }

      fetch(`${this.apiBase}/api/agents/streaming-briefing`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'ngrok-skip-browser-warning': 'true' // Bypass ngrok landing page
        },
        body: JSON.stringify({ cluster_id: clusterId, prompt: prompt })
      }).then(async response => {
        
        if (!response.body) {
          observer.error('Readable stream not supported or response body is null');
          return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');

        try {
          while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
              observer.complete();
              break;
            }

            const chunk = decoder.decode(value, { stream: true });
            
            // SSE format parsing: lines start with "data: "
            const lines = chunk.split('\n');
            
            for (const line of lines) {
              const trimmed = line.trim();
              
              if (trimmed.startsWith('data: ')) {
                const data = trimmed.slice(6); // Remove 'data: ' prefix
                
                if (data === '[DONE]') {
                  observer.complete();
                  return;
                }

                // If content is pure text, emit it.
                // If it's a specific JSON status, you can handle it here too.
                try {
                  const jsonMsg = JSON.parse(data);
                  if (jsonMsg.error) {
                    observer.error(jsonMsg.error);
                    return;
                  }
                } catch (e) {
                  // Not JSON, likely just text content or a token
                  // Use NgZone to ensure Angular detection cycle updates UI immediately
                  this.zone.run(() => observer.next(data));
                }
              }
            }
          }
        } catch (readError) {
          observer.error(readError);
        }

      }).catch(fetchError => {
        observer.error(fetchError);
      });

    });
  }
}
