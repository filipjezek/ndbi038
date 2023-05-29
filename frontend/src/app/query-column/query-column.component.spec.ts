import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QueryColumnComponent } from './query-column.component';

describe('QueryColumnComponent', () => {
  let component: QueryColumnComponent;
  let fixture: ComponentFixture<QueryColumnComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ QueryColumnComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(QueryColumnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
