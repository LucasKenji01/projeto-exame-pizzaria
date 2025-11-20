import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

export interface ItemPedidoResponse {
  id: number;
  produto_id: number | null;
  produto_personalizado_id: number | null;
  quantidade: number;
  preco_unitario: number;
  preco_total: number;
  nome_produto?: string;
  tipo?: string;
}

export interface ItemPedido {
  name: string;
  quantity: number;
  price: number;
}

export interface Pedido {
  id: number;
  descricao: string;
  quantidade: number;
  valor_total: number;
  email: string;
  cliente_id: number;
  data_pedido: string;
  status: string;
  itens?: ItemPedidoResponse[];
}

export interface PedidoRequest {
  descricao?: string;
  email?: string;
}

@Injectable({
  providedIn: 'root'
})
export class PedidosService {
  private apiUrl = 'http://localhost:8000/pedidos';

  constructor(private http: HttpClient, private authService: AuthService) { }

  /**
   * Obter headers com token de autenticação
   */
  private getHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    console.log('🔐 PedidosService: Criando headers com token:', !!token);

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
   * Finalizar pedido (criar novo pedido a partir do carrinho)
   */
  finalizarPedido(pedidoData: PedidoRequest): Observable<Pedido> {
    console.log('📤 PedidosService.finalizarPedido: Iniciando requisição POST /pedidos/finalizar');
    const headers = this.getHeaders();
    console.log('📤 PedidosService: Headers com token?', headers.has('Authorization'));

    return this.http.post<Pedido>(`${this.apiUrl}/finalizar`, pedidoData, { headers });
  }

  /**
   * Listar todos os pedidos do usuário autenticado
   */
  listarMeusPedidos(): Observable<Pedido[]> {
    console.log('📥 PedidosService.listarMeusPedidos: Iniciando requisição GET /pedidos/me');
    const headers = this.getHeaders();
    console.log('📥 PedidosService: Headers com token?', headers.has('Authorization'));

    return this.http.get<Pedido[]>(`${this.apiUrl}/me`, { headers });
  }

  /**
   * Obter um pedido específico por ID
   */
  obterPedidoPorId(pedidoId: number): Observable<Pedido> {
    const headers = this.getHeaders();
    return this.http.get<Pedido>(`${this.apiUrl}/${pedidoId}`, { headers });
  }
}
