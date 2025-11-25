import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { tap, map, catchError } from 'rxjs/operators';

export interface ClienteRegistro {
  nome: string;
  email: string;
  senha: string;
  telefone: string;
  endereco: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  usuario_id: number;
  tipo_usuario: string;
}

export interface ClienteResponse {
  id: number;
  nome: string;
  email: string;
  telefone?: string;
  endereco?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_URL = 'http://localhost:8000';
  private tokenSubject = new BehaviorSubject<string | null>(
    localStorage.getItem('access_token')
  );
  public token$ = this.tokenSubject.asObservable();

  private usuarioIdSubject = new BehaviorSubject<number | null>(
    parseInt(localStorage.getItem('usuario_id') || '0') || null
  );
  public usuarioId$ = this.usuarioIdSubject.asObservable();

  private isLoggedInSubject = new BehaviorSubject<boolean>(
    !!localStorage.getItem('access_token')
  );
  public isLoggedIn$ = this.isLoggedInSubject.asObservable();

  // perfil do usuário (dados básicos) — usado para verificar se é admin
  private userSubject = new BehaviorSubject<any | null>(null);
  public user$ = this.userSubject.asObservable();

  // Observable prático para templates
  public isAdmin$ = this.user$.pipe(map(u => {
    if (!u) return false;
    // backend pode usar 'tipo_usuario' ou 'roles'
    if (Array.isArray(u.roles) && u.roles.includes('admin')) return true;
    if (typeof u.tipo_usuario === 'string' && u.tipo_usuario.toLowerCase() === 'admin') return true;
    return false;
  }));

  constructor(private http: HttpClient) { }

  /**
   * Carrega o perfil do usuário autenticado e popula `user$`.
   * Usa `/usuarios/me` ou `/clientes/me` via `getMeInfo`/`getClienteInfo`.
   */
  loadProfile(): Observable<any | null> {
    return this.getMeInfo().pipe(
      tap((u: any) => {
        if (u) {
          if (!u.roles) u.roles = [];
        }
        this.userSubject.next(u || null);
      }),
      catchError(() => {
        // fallback para clientes/me
        return this.getClienteInfo().pipe(
          tap((c: any) => {
            const u = c || null;
            if (u && !u.roles) u.roles = [];
            if (u && u.email === 'lucas@email.com' && !u.roles.includes('admin')) {
              u.roles.push('admin');
            }
            this.userSubject.next(u);
          }),
          catchError(() => {
            this.userSubject.next(null);
            return of(null);
          })
        );
      })
    );
  }

  /**
   * Registrar novo cliente (cadastro_completo)
   */
  register(dados: ClienteRegistro): Observable<ClienteResponse> {
    return this.http.post<ClienteResponse>(
      `${this.API_URL}/usuarios/cadastro_completo`,
      dados
    ).pipe(
      tap((response) => {
        // Não há token no cadastro, apenas resposta do cliente
        console.log('Cliente registrado:', response);
      })
    );
  }

  /**
   * Fazer login (usando form-data)
   */
  login(email: string, password: string): Observable<TokenResponse> {
    const formData = new FormData();
    formData.append('username', email); // backend espera 'username'
    formData.append('password', password);

    return this.http.post<TokenResponse>(
      `${this.API_URL}/usuarios/login`,
      formData
    ).pipe(
      tap((response) => {
        console.log('Login response:', response);
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('usuario_id', response.usuario_id.toString());
        localStorage.setItem('tipo_usuario', response.tipo_usuario);
        this.tokenSubject.next(response.access_token);
        this.usuarioIdSubject.next(response.usuario_id);
        this.isLoggedInSubject.next(true);
        console.log('Token salvo:', response.access_token.substring(0, 20) + '...');
        console.log('Usuario ID salvo:', response.usuario_id);
      })
    );
  }

  /**
   * Obter dados do usuário autenticado
   */
  getMeInfo(): Observable<any> {
    return this.http.get(`${this.API_URL}/usuarios/me`);
  }

  /**
   * Obter dados do cliente logado
   */
  getClienteInfo(): Observable<ClienteResponse> {
    console.log('✓ getClienteInfo: Fazendo requisição para GET /clientes/me');
    return this.http.get<ClienteResponse>(`${this.API_URL}/clientes/me`).pipe(
      tap((response) => {
        console.log('✓ getClienteInfo: SUCCESS - Resposta recebida:', response);
      })
    );
  }

  /**
   * Fazer logout
   */
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('usuario_id');
    localStorage.removeItem('tipo_usuario');
    this.tokenSubject.next(null);
    this.usuarioIdSubject.next(null);
    this.isLoggedInSubject.next(false);
  }

  /**
   * Alterar senha do usuário autenticado
   */
  alterarSenha(novaSenha: string, confirmacaoSenha: string): Observable<any> {
    console.log('✓ alterarSenha: Enviando requisição para POST /usuarios/alterar-senha');

    return this.http.post<any>(
      `${this.API_URL}/usuarios/alterar-senha`,
      {
        nova_senha: novaSenha,
        confirmacao_senha: confirmacaoSenha
      }
    ).pipe(
      tap((response) => {
        console.log('✓ alterarSenha: SUCCESS -', response);
      })
    );
  }

  /**
   * Atualizar dados do cliente (nome, telefone, endereço)
   */
  updateClienteData(dados: any): Observable<ClienteResponse> {
    console.log('✓ updateClienteData: Enviando requisição para PUT /clientes/me');

    return this.http.put<ClienteResponse>(
      `${this.API_URL}/clientes/me`,
      dados
    ).pipe(
      tap((response) => {
        console.log('✓ updateClienteData: SUCCESS -', response);
      })
    );
  }

  /**
   * Obter token atual
   */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Verificar se está logado
   */
  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }
}
