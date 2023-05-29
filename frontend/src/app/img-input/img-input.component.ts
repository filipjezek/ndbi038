import { Component, forwardRef } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { UnsubscribingComponent } from '../unsubscribing.mixin';
import { switchMap } from 'rxjs/operators';
import { from } from 'rxjs';

@Component({
  selector: 'ndbi038-img-input',
  templateUrl: './img-input.component.html',
  styleUrls: ['./img-input.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => ImgInputComponent),
      multi: true,
    },
  ],
})
export class ImgInputComponent
  extends UnsubscribingComponent
  implements ControlValueAccessor
{
  onTouchedCb: () => void;
  private onChangeCb: (val: string) => void;
  disabled = false;
  public get value() {
    return this._value;
  }
  private _value: string;

  writeValue(obj: string): void {
    this._value = obj;
  }
  registerOnChange(fn: any): void {
    this.onChangeCb = fn;
  }
  registerOnTouched(fn: any): void {
    this.onTouchedCb = fn;
  }
  setDisabledState?(isDisabled: boolean): void {
    this.disabled = isDisabled;
  }

  onControlChange(file: File) {
    if (!file) {
      this._value = null;
      this.onChangeCb(this.value);
      return;
    }

    from(
      new Promise<string>((res, rej) => {
        const fr = new FileReader();
        fr.onerror = (err) => rej(err);
        fr.onload = () => res(fr.result.toString());
        fr.readAsDataURL(file);
      })
    )
      .pipe(
        switchMap((url) =>
          from(
            new Promise<HTMLImageElement>((res, rej) => {
              const img = new Image();
              img.onload = () => res(img);
              img.src = url;
            })
          )
        )
      )
      .subscribe((img) => {
        const canvas = document.createElement('canvas');
        canvas.width = 100;
        canvas.height = 100;
        const ctx = canvas.getContext('2d');
        const size = Math.min(img.width, img.height);
        ctx.drawImage(
          img,
          (img.width - size) / 2,
          (img.height - size) / 2,
          size,
          size,
          0,
          0,
          100,
          100
        );
        this._value = canvas.toDataURL();
        this.onChangeCb(this.value);
      });
  }
}
