import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { CreatePizzaComponent } from './pages/create-pizza/create-pizza.component';
import { OrdersComponent } from './pages/orders/orders.component';
import { AccountComponent } from './pages/account/account.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'create-pizza',
    component: CreatePizzaComponent
  },
  {
    path: 'orders',
    component: OrdersComponent
  },
  {
    path: 'account',
    component: AccountComponent
  },
];
