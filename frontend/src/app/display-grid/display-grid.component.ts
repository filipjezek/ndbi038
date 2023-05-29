import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'ndbi038-display-grid',
  templateUrl: './display-grid.component.html',
  styleUrls: ['./display-grid.component.scss'],
})
export class DisplayGridComponent implements OnInit {
  @Input() images: string[] = [];
  @Input() cols: number;

  range: number[];

  constructor() {}

  ngOnInit(): void {}
}
