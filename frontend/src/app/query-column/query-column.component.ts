import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { RadioOption } from '../button-radio/button-radio.component';
import { DisplayType } from '../services/display.service';
import { UnsubscribingComponent } from '../unsubscribing.mixin';
import { exactlyOne } from '../utils/exactly-one.validator';
import { startWith, takeUntil } from 'rxjs';

export interface Query {
  text?: string;
  image?: string;
  k: number;
  displayType: DisplayType;
}

@Component({
  selector: 'ndbi038-query-column',
  templateUrl: './query-column.component.html',
  styleUrls: ['./query-column.component.scss'],
})
export class QueryColumnComponent
  extends UnsubscribingComponent
  implements OnInit
{
  @Output() query = new EventEmitter<Query>();

  queryForm = this.fb.group(
    {
      text: '',
      image: '',
      k: [25, [Validators.required, Validators.min(1)]],
      displayType: [DisplayType.topK, Validators.required],
    },
    { validators: [exactlyOne(/^text|image$/)] }
  );

  displayTypes: RadioOption[] = [
    { label: 'top k', value: DisplayType.topK },
    { label: 'top k - golden triangle', value: DisplayType.topKTriangle },
  ];
  queryTypes: RadioOption[] = [
    { label: 'text', value: 'text' },
    { label: 'image', value: 'image' },
  ];
  queryTypeCtrl = new FormControl('text');

  constructor(private fb: FormBuilder) {
    super();
  }

  ngOnInit(): void {
    this.queryTypeCtrl.valueChanges
      .pipe(startWith(this.queryTypeCtrl.value), takeUntil(this.onDestroy$))
      .subscribe((val) => {
        ['text', 'image'].forEach((key) =>
          this.queryForm.get(key)[key == val ? 'enable' : 'disable']()
        );
      });
  }

  submitQuery() {
    this.query.emit(this.queryForm.value as Query);
  }
}
