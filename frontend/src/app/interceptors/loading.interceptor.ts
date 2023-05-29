import { Injectable, InjectionToken } from '@angular/core';
import {
  HttpEvent,
  HttpInterceptor,
  HttpHandler,
  HttpRequest,
} from '@angular/common/http';

import { BehaviorSubject, Observable } from 'rxjs';
import { auditTime, finalize, map } from 'rxjs/operators';

const loadingSubj = new BehaviorSubject<number>(0);
export const HTTP_LOADING = new InjectionToken<Observable<boolean>>(
  'Http loading',
  {
    factory: () =>
      loadingSubj.pipe(
        map((num) => num > 0),
        auditTime(5)
      ),
  }
);

@Injectable()
export class LoadingInterceptor implements HttpInterceptor {
  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    loadingSubj.next(loadingSubj.value + 1);
    return next.handle(req).pipe(
      finalize(() => {
        loadingSubj.next(loadingSubj.value - 1);
      })
    );
  }
}
