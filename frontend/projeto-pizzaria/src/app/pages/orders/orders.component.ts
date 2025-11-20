import { AsyncPipe, CommonModule, NgForOf } from '@angular/common';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterLink } from "@angular/router";
import { TuiFormatNumberPipe } from '@taiga-ui/core';
import { TuiTable } from '@taiga-ui/addon-table';
import { TuiCell } from "@taiga-ui/layout";
import { PedidosService, Pedido, ItemPedido } from '../../services/pedidos.service';
import { Subscription } from 'rxjs';

// Tipos para a tabela
interface OrderRow {
  orderId: number;
  order: ItemPedido[];
  data: string;
  status: string;
}

@Component({
  selector: 'app-orders',
  imports: [CommonModule, RouterLink, TuiTable, NgForOf],
  templateUrl: './orders.component.html',
  styleUrl: './orders.component.css'
})
export class OrdersComponent implements OnInit, OnDestroy {
  protected data: OrderRow[] = [];
  protected readonly columns: string[] = ['orderId', 'order', 'price', 'data', 'status'];

  private pedidosSubscription?: Subscription;
  isLoading: boolean = false;

  constructor(private pedidosService: PedidosService) { }

  ngOnInit(): void {
    this.carregarPedidos();
  }

  /**
   * Carregar pedidos do backend
   */
  carregarPedidos(): void {
    this.isLoading = true;
    console.log('📋 OrdersComponent: Carregando pedidos...');

    this.pedidosSubscription = this.pedidosService.listarMeusPedidos().subscribe({
      next: (pedidos: Pedido[]) => {
        console.log('✓ OrdersComponent: Pedidos carregados:', pedidos.length);

        // Transformar pedidos da API para o formato da tabela
        this.data = pedidos.map(pedido => {
          // Se itens existem na resposta, usar; senão, criar item com base na descrição
          let items: ItemPedido[] = [];

          if (pedido.itens && pedido.itens.length > 0) {
            items = pedido.itens.map(item => ({
              name: item.nome_produto || 'Pizza',
              quantity: item.quantidade,
              price: item.preco_unitario
            }));
          } else {
            // Fallback: criar um item único com a informação do pedido
            items = [{
              name: pedido.descricao || 'Pedido',
              quantity: pedido.quantidade,
              price: pedido.valor_total / pedido.quantidade
            }];
          }

          // Formatar data
          const dataPedido = new Date(pedido.data_pedido);
          const dataFormatada = dataPedido.toLocaleDateString('pt-BR') + ' ' + dataPedido.toLocaleTimeString('pt-BR');

          return {
            orderId: pedido.id,
            order: items,
            data: dataFormatada,
            status: this.traduzirStatus(pedido.status)
          };
        });

        console.log(`✨ ${this.data.length} pedidos convertidos para a tabela`);
        this.isLoading = false;
      },
      error: (error) => {
        console.error('❌ OrdersComponent: Erro ao carregar pedidos:', error);
        this.isLoading = false;
      }
    });
  }

  /**
   * Traduzir status do pedido para português
   */
  traduzirStatus(status: string): string {
    const statusMap: { [key: string]: string } = {
      'pendente': 'Pendente',
      'em_producao': 'Em produção',
      'pronto': 'Pronto',
      'saiu_entrega': 'Saiu para entrega',
      'entregue': 'Entregue',
      'cancelado': 'Cancelado'
    };
    return statusMap[status.toLowerCase()] || status;
  }

  public getOrderPrice(row: OrderRow): number {
    return row.order.reduce((sum, item) => sum + (item.quantity * item.price), 0);
  }

  ngOnDestroy(): void {
    if (this.pedidosSubscription) {
      this.pedidosSubscription.unsubscribe();
    }
  }
}
