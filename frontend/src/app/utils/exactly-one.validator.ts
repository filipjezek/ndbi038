import { AbstractControl, FormGroup, ValidationErrors } from '@angular/forms';

export const exactlyOne =
  (selector?: RegExp) =>
  (control: AbstractControl): ValidationErrors | null => {
    const group = control as FormGroup;
    const applicable = Object.entries(group.controls)
      .filter(
        ([key, ctrl]) => (!selector || selector.test(key)) && ctrl.enabled
      )
      .map(([key, ctrl]) => ctrl);

    return applicable.filter((c) => c.value).length === 1
      ? null
      : { exactlyOne: true };
  };
