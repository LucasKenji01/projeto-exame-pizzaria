import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { CreatePizzaComponent } from './pages/create-pizza/create-pizza.component';
import { OrdersComponent } from './pages/orders/orders.component';
import { AccountComponent } from './pages/account/account.component';
import { AdminComponent } from './pages/admin/admin.component';
import { AdminGuard } from './guards/admin.guard';
import { AdminDashboardComponent } from './pages/admin/dashboard/dashboard.component';
import { AdminPedidosComponent } from './pages/admin/pedidos/pedidos.component';
import { AdminProdutosComponent } from './pages/admin/produtos/produtos.component';

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
    path: 'admin',
    component: AdminComponent,
    canActivate: [AdminGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: AdminDashboardComponent },
      { path: 'pedidos', component: AdminPedidosComponent },
      { path: 'produtos', component: AdminProdutosComponent },
    ]
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
