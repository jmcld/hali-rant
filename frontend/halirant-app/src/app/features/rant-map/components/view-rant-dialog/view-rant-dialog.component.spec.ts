import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewRantDialogComponent } from './view-rant-dialog.component';

describe('ViewRantDialogComponent', () => {
  let component: ViewRantDialogComponent;
  let fixture: ComponentFixture<ViewRantDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewRantDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewRantDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
