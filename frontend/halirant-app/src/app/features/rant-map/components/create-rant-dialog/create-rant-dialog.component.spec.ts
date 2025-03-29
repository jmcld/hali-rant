import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateRantDialogComponent } from './create-rant-dialog.component';

describe('CreateRantDialogComponent', () => {
  let component: CreateRantDialogComponent;
  let fixture: ComponentFixture<CreateRantDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateRantDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateRantDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
