import { Injectable } from '@angular/core';
import { HttpService } from './http.service';
import { Query } from '../query-column/query-column.component';

export enum DisplayType {
  topK = 'topk',
  topKTriangle = 'topk_triangle',
}

@Injectable({
  providedIn: 'root',
})
export class DisplayService {
  constructor(private http: HttpService) {}

  sendQuery(query: Omit<Query, 'k'> & { width: number; height: number }) {
    if (!query.text === !query.image) {
      throw new Error('you have to provide exactly one mode of query');
    }
    return this.http.post<string[]>('query', query);
  }
}
