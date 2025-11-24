import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

  constructor(private http: HttpClient) { }

  /**
   * Finalizar pedido (criar novo pedido a partir do carrinho)
   */
  finalizarPedido(pedidoData: PedidoRequest): Observable<Pedido> {
    console.log('📤 PedidosService.finalizarPedido: Iniciando requisição POST /pedidos/finalizar');

    return this.http.post<Pedido>(`${this.apiUrl}/finalizar`, pedidoData);
  }

  /**
   * Listar todos os pedidos do usuário autenticado
   */
  listarMeusPedidos(): Observable<Pedido[]> {
    console.log('📥 PedidosService.listarMeusPedidos: Iniciando requisição GET /pedidos/me');

    return this.http.get<Pedido[]>(`${this.apiUrl}/me`);
  }

  /**
   * Obter um pedido específico por ID
   */
  obterPedidoPorId(pedidoId: number): Observable<Pedido> {
    return this.http.get<Pedido>(`${this.apiUrl}/${pedidoId}`);
  }
}
