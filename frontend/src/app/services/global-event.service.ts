import { Injectable, Inject } from '@angular/core';
import { Observable, fromEvent, animationFrameScheduler } from 'rxjs';
import { filter, observeOn } from 'rxjs/operators';
import { DOCUMENT } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class GlobalEventService {
  public documentClicked: Observable<MouseEvent>;
  public keyPressed: Observable<KeyboardEvent>;
  public enterPressed: Observable<KeyboardEvent>;
  public spacePressed: Observable<KeyboardEvent>;
  public escapePressed: Observable<KeyboardEvent>;
  public nonBlockingScroll: Observable<Event>;
  public nonBlockingDrag: Observable<MouseEvent>;
  public nonBlockingResize: Observable<UIEvent>;
  public mouseReleased: Observable<MouseEvent>;

  constructor(@Inject(DOCUMENT) private doc: Document) {
    this.documentClicked = fromEvent<MouseEvent>(this.doc, 'click');

    this.keyPressed = fromEvent<KeyboardEvent>(this.doc, 'keydown');
    this.enterPressed = this.keyPressed.pipe(
      filter((e) => e.which === 13 || e.key === 'Enter')
    );
    this.spacePressed = this.keyPressed.pipe(
      filter((e) => e.which === 32 || e.key === ' ' || e.key === 'Spacebar')
    );
    this.escapePressed = this.keyPressed.pipe(
      filter((e) => e.which === 27 || e.key === 'Escape')
    );
    this.nonBlockingScroll = fromEvent(this.doc, 'scroll', {
      passive: true,
    }).pipe(observeOn(animationFrameScheduler));
    this.nonBlockingDrag = fromEvent<MouseEvent>(this.doc, 'mousemove').pipe(
      observeOn(animationFrameScheduler)
    );
    this.nonBlockingResize = fromEvent<UIEvent>(window, 'resize', {
      passive: true,
    }).pipe(observeOn(animationFrameScheduler));
    this.mouseReleased = fromEvent<MouseEvent>(this.doc, 'mouseup');
  }
}
