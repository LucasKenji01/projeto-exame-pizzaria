import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class CarrinhoService {
  private apiUrl = 'http://localhost:8000/carrinho';

  // BehaviorSubject para rastrear quantidade total de itens
  private cartCountSubject = new BehaviorSubject<number>(0);
  public cartCount$ = this.cartCountSubject.asObservable();

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {
    // Carregar contagem inicial ao inicializar o serviço
    this.carregarContagem();
  }

  /**
   * Carregar contagem inicial do carrinho
   */
  private carregarContagem(): void {
    this.listarCarrinho().subscribe({
      next: (items: any[]) => {
        const total = items.reduce((acc, item) => acc + (item.quantidade || 0), 0);
        this.cartCountSubject.next(total);
      },
      error: () => this.cartCountSubject.next(0)
    });
  }

  /**
   * Obter headers com token JWT
   */
  private getHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    if (token) {
      return new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      });
    }
    return new HttpHeaders({
      'Content-Type': 'application/json'
    });
  }

  /**
   * Atualizar contagem interna
   */
  private atualizarContagem(quantidade: number): void {
    this.cartCountSubject.next(quantidade);
  }

  /**
   * Adicionar item ao carrinho
   */
  adicionarItem(item: { produto_id?: number; produto_personalizado_id?: number; quantidade: number }): Observable<any> {
    const headers = this.getHeaders();
    return this.http.post<any>(`${this.apiUrl}/adicionar`, item, { headers }).pipe(
      tap(() => {
        // Recarregar contagem após adicionar
        this.listarCarrinho().subscribe(
          items => {
            const total = items.reduce((acc, i) => acc + (i.quantidade || 0), 0);
            this.atualizarContagem(total);
          }
        );
      }),
      catchError((error: any) => {
        console.error('❌ Erro ao adicionar item:', error);
        throw error;
      })
    );
  }

  /**
   * Listar itens do carrinho (simples)
   */
  listarCarrinho(): Observable<any[]> {
    const headers = this.getHeaders();
    return this.http.get<any[]>(`${this.apiUrl}/`, { headers });
  }

  /**
   * Listar carrinho com detalhes completos dos produtos
   */
  listarCarrinhoDetalhado(): Observable<any> {
    const headers = this.getHeaders();
    return this.http.get<any>(`${this.apiUrl}/detalhado`, { headers });
  }

  /**
   * Remover item do carrinho
   */
  removerItem(itemId: number): Observable<any> {
    const headers = this.getHeaders();
    const url = `${this.apiUrl}/${itemId}`;
    console.log('🔍 DEBUG removerItem:', { itemId, url, headers: headers.keys() });
    return this.http.delete<any>(url, { headers }).pipe(
      tap((response: any) => {
        console.log('✅ DELETE sucesso:', response);
        // Recarregar contagem após deletar
        this.listarCarrinho().subscribe(
          items => {
            const total = items.reduce((acc, i) => acc + (i.quantidade || 0), 0);
            this.atualizarContagem(total);
          }
        );
      }),
      catchError((error: any) => {
        console.error('❌ DELETE erro:', { itemId, url, status: error.status, error });
        throw error;
      })
    );
  }

  /**
   * Limpar todo o carrinho
   */
  limparCarrinho(): Observable<any> {
    const headers = this.getHeaders();
    const url = `${this.apiUrl}/limpar`;
    console.log('🔍 DEBUG limparCarrinho:', { url });
    return this.http.delete<any>(url, { headers }).pipe(
      tap(() => {
        this.atualizarContagem(0);
      })
    );
  }
}
