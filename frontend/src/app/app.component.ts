import { transition, trigger, useAnimation } from '@angular/animations';
import {
  Component,
  ElementRef,
  Inject,
  OnInit,
  ViewChild,
} from '@angular/core';
import { Observable } from 'rxjs';
import { fade } from './animations';
import { HTTP_LOADING } from './interceptors/loading.interceptor';
import { DialogService } from './services/dialog.service';
import { DisplayService } from './services/display.service';
import { UnsubscribingComponent } from './unsubscribing.mixin';
import { Query } from './query-column/query-column.component';

@Component({
  selector: 'ndbi038-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations: [
    trigger('fade', [
      transition(
        ':enter',
        useAnimation(fade, {
          params: {
            start: '0',
            end: '1',
            time: '0.1s',
          },
        })
      ),
      transition(
        ':leave',
        useAnimation(fade, {
          params: {
            start: '1',
            end: '0',
            time: '0.1s',
          },
        })
      ),
    ]),
  ],
})
export class AppComponent extends UnsubscribingComponent implements OnInit {
  @ViewChild('grid', { read: ElementRef })
  private grid: ElementRef<HTMLElement>;
  imgColumns = 5;
  images: string[] = [];
  showOverlay$: Observable<boolean>;

  constructor(
    @Inject(HTTP_LOADING) public loading$: Observable<boolean>,
    private displayS: DisplayService,
    private dialogS: DialogService
  ) {
    super();
    this.showOverlay$ = this.dialogS.showOverlay$;
  }

  ngOnInit(): void {}

  private computeDisplay(size: number) {
    const ratio =
      this.grid.nativeElement.clientWidth /
      this.grid.nativeElement.clientHeight;

    // ratio = w / h
    // w * h = size
    const height = Math.ceil(Math.sqrt(size / ratio));
    const width = Math.ceil(size / height);
    return { width, height };
  }

  sendQuery(query: Query) {
    const q = {
      ...query,
      ...this.computeDisplay(query.k),
    };
    delete q.k;

    this.displayS.sendQuery(q).subscribe((images) => {
      this.images = images;
      this.imgColumns = q.width;
    });
  }
}
