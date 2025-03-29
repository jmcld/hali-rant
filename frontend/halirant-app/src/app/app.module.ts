import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { NavbarComponent } from './core/components/navbar/navbar.component';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [AppComponent, NavbarComponent],
  bootstrap: [AppComponent],
  imports: [AppRoutingModule, CommonModule, BrowserModule, RouterModule],
})
export class AppModule {}
