import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RantMapComponent } from './rant-map.component';

describe('RantMapComponent', () => {
  let component: RantMapComponent;
  let fixture: ComponentFixture<RantMapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RantMapComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RantMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
