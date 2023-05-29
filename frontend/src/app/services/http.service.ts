import { Injectable } from '@angular/core';
import { Observable, throwError, of, BehaviorSubject } from 'rxjs';
import {
  HttpClient,
  HttpErrorResponse,
  HttpParams,
} from '@angular/common/http';
import { retryWhen, concatMap, delay, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private static readonly apiUrl = 'http://127.0.0.1:5000/api/';

  private retryPipeline = retryWhen<any>((err) =>
    err.pipe(
      concatMap((e: HttpErrorResponse, i) => {
        if (i > 5 || ![503, 504, 0, 429, 425].includes(e.status)) {
          return throwError(e.error);
        }
        return of(e).pipe(delay(i * 500));
      })
    )
  );

  constructor(private http: HttpClient) {}

  get<T>(url: string, params?: HttpParams): Observable<T> {
    return this.http
      .get<T>(HttpService.apiUrl + url, {
        params,
      })
      .pipe(this.retryPipeline);
  }

  post<T>(url: string, body: any): Observable<T> {
    return this.http
      .post<T>(HttpService.apiUrl + url, body)
      .pipe(this.retryPipeline);
  }

  put(url: string, body: any): Observable<void> {
    return this.http
      .put<void>(HttpService.apiUrl + url, body)
      .pipe(this.retryPipeline);
  }

  delete(url: string, params?: HttpParams): Observable<void> {
    return this.http
      .delete<void>(HttpService.apiUrl + url, {
        params: params,
      })
      .pipe(this.retryPipeline);
  }
}
