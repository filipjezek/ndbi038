import { BrowserModule } from '@angular/platform-browser';
import { ElementRef, Injector, NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { DisplayGridComponent } from './display-grid/display-grid.component';
import { QueryColumnComponent } from './query-column/query-column.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ButtonRadioComponent } from './button-radio/button-radio.component';
import { LoadingOverlayComponent } from './loading-overlay/loading-overlay.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { LoadingInterceptor } from './interceptors/loading.interceptor';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { KeyboardClickDirective } from './keyboard-click.directive';
import { OverlayComponent } from './overlay/overlay.component';
import { Dialog } from './dialog';
import { createCustomElement } from '@angular/elements';
import { ImgInputComponent } from './img-input/img-input.component';

const customEls: ((new (el: ElementRef, ...args: any[]) => Dialog) & {
  selector: string;
})[] = [];

@NgModule({
  declarations: [
    AppComponent,
    DisplayGridComponent,
    QueryColumnComponent,
    ButtonRadioComponent,
    LoadingOverlayComponent,
    KeyboardClickDirective,
    OverlayComponent,
    ImgInputComponent,
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    HttpClientModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: LoadingInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {
  constructor(injector: Injector) {
    customEls.forEach((el) => {
      const custEl = createCustomElement<Dialog>(el, { injector });
      customElements.define(el.selector, custEl);
    });
  }
}
