import { Component } from '@angular/core';
import { FormAuthComponent } from "../../components/form-auth/form-auth.component";
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormAuthComponent, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

}
