import {
  AbstractControl,
  FormArray,
  ValidationErrors,
  ValidatorFn,
} from '@angular/forms';

export const atLeastOne: ValidatorFn = (
  control: AbstractControl
): ValidationErrors | null => {
  const array = control as FormArray;

  return array.controls.some((c) => c.value) ? null : { noneSelected: true };
};
