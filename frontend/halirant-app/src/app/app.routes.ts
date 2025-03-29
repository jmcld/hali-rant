import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { AboutComponent } from './features/about/about.component';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: '', redirectTo:'home'},
  { path: 'about', component: AboutComponent },
  { path: '**', component: HomeComponent }, // 404
];
