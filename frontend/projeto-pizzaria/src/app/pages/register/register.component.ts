import { Component } from '@angular/core';
import { FormAuthComponent } from '../../components/form-auth/form-auth.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [FormAuthComponent, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

}
