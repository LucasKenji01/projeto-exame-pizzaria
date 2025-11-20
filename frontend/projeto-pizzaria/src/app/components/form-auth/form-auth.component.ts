import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TuiIcon, TuiTextfield, TuiButton } from "@taiga-ui/core";
import { TuiPassword } from '@taiga-ui/kit';
import { AuthService, ClienteRegistro } from '../../services/auth.service';

@Component({
  selector: 'app-form-auth',
  standalone: true,
  imports: [CommonModule, FormsModule, TuiTextfield, TuiPassword, TuiIcon, TuiButton],
  templateUrl: './form-auth.component.html',
  styleUrl: './form-auth.component.css'
})
export class FormAuthComponent {
  email: string = '';
  password: string = '';
  nome: string = '';
  telefone: string = '';
  endereco: string = '';

  @Input() formType: 'login' | 'register' = 'login';

  isLoading: boolean = false;
  errorMessage: string = '';
  successMessage: string = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  /**
   * Submeter formulário (login ou registro)
   */
  onSubmit(): void {
    if (this.formType === 'login') {
      this.handleLogin();
    } else {
      this.handleRegister();
    }
  }

  /**
   * Processar login
   */
  private handleLogin(): void {
    if (!this.email || !this.password) {
      this.errorMessage = 'Email e senha são obrigatórios';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.login(this.email, this.password).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.successMessage = 'Login realizado com sucesso!';
        console.log('Login bem-sucedido:', response);
        setTimeout(() => {
          this.router.navigate(['/home']);
        }, 1000);
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.error?.detail || 'Erro ao fazer login';
        console.error('Erro no login:', error);
      }
    });
  }

  /**
   * Processar registro
   */
  private handleRegister(): void {
    if (!this.nome || !this.email || !this.password || !this.telefone || !this.endereco) {
      this.errorMessage = 'Todos os campos são obrigatórios';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const dados: ClienteRegistro = {
      nome: this.nome,
      email: this.email,
      senha: this.password,
      telefone: this.telefone,
      endereco: this.endereco
    };

    this.authService.register(dados).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.successMessage = 'Cadastro realizado com sucesso! Faça login para continuar.';
        console.log('Cadastro bem-sucedido:', response);
        // Limpar formulário
        this.limparFormulario();
        // Depois de 2s, redirecionar para login
        setTimeout(() => {
          this.formType = 'login';
          this.successMessage = '';
        }, 2000);
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.error?.detail || 'Erro ao registrar usuário';
        console.error('Erro no registro:', error);
      }
    });
  }

  /**
   * Limpar formulário
   */
  private limparFormulario(): void {
    this.email = '';
    this.password = '';
    this.nome = '';
    this.telefone = '';
    this.endereco = '';
  }
}
