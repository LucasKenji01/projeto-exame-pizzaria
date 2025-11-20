import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, Router } from "@angular/router";
import { TuiIcon, TuiTextfield, TuiButton } from "@taiga-ui/core";
import { TuiPassword } from '@taiga-ui/kit';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-account',
  imports: [CommonModule, FormsModule, RouterLink, TuiTextfield, TuiIcon, TuiPassword, TuiButton],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent implements OnInit {

  user = {
    fullname: '',
    email: '',
    telefone: '',
    endereco: ''
  }

  // Campo de senha separado - não carregado do backend por segurança
  newPassword = '';
  confirmPassword = '';

  isLoading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    // Verificar se o usuário está logado antes de carregar dados
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }
    this.loadClienteData();
  }

  loadClienteData(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    // Verificar se há token antes de fazer a requisição
    const token = this.authService.getToken();
    console.log('AccountComponent: Token encontrado?', !!token);
    console.log('AccountComponent: Token value', token ? token.substring(0, 20) + '...' : 'null');

    if (!token) {
      this.errorMessage = 'Você precisa estar logado para acessar esta página';
      this.isLoading = false;
      setTimeout(() => {
        this.router.navigate(['/login']);
      }, 2000);
      return;
    }

    console.log('AccountComponent: Fazendo requisição para /clientes/me');
    console.log('AccountComponent: Token completo:', token);

    this.authService.getClienteInfo().subscribe({
      next: (cliente) => {
        console.log('AccountComponent: Sucesso ao carregar dados do cliente:', cliente);
        this.user.fullname = cliente.nome || '';
        this.user.email = cliente.email || '';
        this.user.telefone = cliente.telefone || '';
        this.user.endereco = cliente.endereco || '';
        // Nota: senha não é carregada por segurança. O usuário pode mudar no campo de "nova senha"
        this.isLoading = false;
      },
      error: (error) => {
        console.error('AccountComponent: Erro ao carregar dados do cliente:', error);
        console.error('AccountComponent: Erro status:', error.status);
        console.error('AccountComponent: Erro message:', error.message);
        console.error('AccountComponent: Erro responseText:', error.error);

        if (error.status === 401) {
          this.errorMessage = 'Sessão expirada. Redirecionando para login...';
          // Limpar dados de autenticação
          this.authService.logout();
          // Redirecionar para login após 2 segundos
          setTimeout(() => {
            this.router.navigate(['/login']);
          }, 2000);
        } else {
          this.errorMessage = 'Erro ao carregar dados do cliente. Tente novamente.';
        }
        this.isLoading = false;
      }
    });
  }

  /**
   * Salvar dados do usuário (nome, email, telefone, endereço)
   */
  saveUserData(): void {
    this.errorMessage = '';
    this.successMessage = '';

    // Validações básicas
    if (!this.user.fullname.trim()) {
      this.errorMessage = 'Nome é obrigatório';
      return;
    }

    if (!this.user.email.trim()) {
      this.errorMessage = 'Email é obrigatório';
      return;
    }

    this.isLoading = true;
    console.log('AccountComponent: Iniciando salvamento de dados do cliente');

    const dadosAtualizacao = {
      telefone: this.user.telefone || '',
      endereco: this.user.endereco || ''
    };

    this.authService.updateClienteData(dadosAtualizacao).subscribe({
      next: (response) => {
        console.log('AccountComponent: Sucesso ao salvar dados:', response);
        this.successMessage = 'Dados salvos com sucesso!';
        this.isLoading = false;

        // Limpar mensagem após 3 segundos
        setTimeout(() => {
          this.successMessage = '';
        }, 3000);
      },
      error: (error) => {
        console.error('AccountComponent: Erro ao salvar dados:', error);
        console.error('AccountComponent: Erro status:', error.status);

        // Extrair mensagem de erro do backend
        if (error.error && error.error.detail) {
          this.errorMessage = error.error.detail;
        } else if (error.error && typeof error.error === 'string') {
          this.errorMessage = error.error;
        } else {
          this.errorMessage = 'Erro ao salvar dados. Tente novamente.';
        }

        this.isLoading = false;
      }
    });
  }

  /**
   * Mudar senha do usuário
   */
  changePassword(): void {
    this.errorMessage = '';
    this.successMessage = '';

    // Validações
    if (!this.newPassword.trim()) {
      this.errorMessage = 'Nova senha é obrigatória';
      return;
    }

    if (!this.confirmPassword.trim()) {
      this.errorMessage = 'Confirmação de senha é obrigatória';
      return;
    }

    if (this.newPassword !== this.confirmPassword) {
      this.errorMessage = 'As senhas não conferem';
      return;
    }

    if (this.newPassword.length < 6) {
      this.errorMessage = 'Senha deve ter no mínimo 6 caracteres';
      return;
    }

    this.isLoading = true;
    console.log('AccountComponent: Iniciando alteração de senha');

    this.authService.alterarSenha(this.newPassword, this.confirmPassword).subscribe({
      next: (response) => {
        console.log('AccountComponent: Sucesso ao alterar senha:', response);
        this.successMessage = response.mensagem || 'Senha alterada com sucesso!';
        this.newPassword = '';
        this.confirmPassword = '';
        this.isLoading = false;

        // Limpar mensagem após 3 segundos
        setTimeout(() => {
          this.successMessage = '';
        }, 3000);
      },
      error: (error) => {
        console.error('AccountComponent: Erro ao alterar senha:', error);
        console.error('AccountComponent: Erro status:', error.status);
        console.error('AccountComponent: Erro message:', error.message);

        // Extrair mensagem de erro do backend
        if (error.error && error.error.detail) {
          this.errorMessage = error.error.detail;
        } else if (error.error && typeof error.error === 'string') {
          this.errorMessage = error.error;
        } else {
          this.errorMessage = 'Erro ao alterar senha. Tente novamente.';
        }

        this.isLoading = false;
      }
    });
  }

}
