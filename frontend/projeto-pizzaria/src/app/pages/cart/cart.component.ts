import { Component, Input, WritableSignal, Output, EventEmitter, OnInit } from '@angular/core';
import { TuiPopup, TuiButton, TuiIcon } from '@taiga-ui/core';
import { TuiDrawer } from '@taiga-ui/kit';
import { CommonModule } from '@angular/common';
import { PedidosService } from '../../services/pedidos.service';
import { AuthService } from '../../services/auth.service';
import { CarrinhoService } from '../../services/carrinho.service';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, TuiDrawer, TuiPopup, TuiButton, TuiIcon],
  templateUrl: './cart.component.html',
  styleUrl: './cart.component.css'
})
export class CartComponent implements OnInit {
  @Input() open!: WritableSignal<boolean>;
  @Output() pedidoFinalizado = new EventEmitter<void>();

  deliveryFee: number = 10;
  isLoading: boolean = false;

  cartItems: any[] = [];

  constructor(
    private pedidosService: PedidosService,
    private authService: AuthService,
    private carrinhoService: CarrinhoService
  ) { }

  ngOnInit(): void {
    // Carregar itens do carrinho ao inicializar
    this.carregarCarrinho();
  }

  /**
   * Carregar itens do carrinho do backend
   */
  carregarCarrinho(): void {
    console.log('📦 CarrinhoComponent: Carregando carrinho do backend...');
    this.carrinhoService.listarCarrinhoDetalhado().subscribe({
      next: (response) => {
        console.log('📦 Carrinho carregado:', response);
        this.cartItems = response.itens || [];
      },
      error: (error) => {
        console.error('❌ Erro ao carregar carrinho:', error);
        this.cartItems = [];
      }
    });
  }

  addItem(item: { name: string; description?: string; quantity: number; price: number }) {
    const existingItem = this.cartItems.find(cartItem => cartItem.name === item.name);

    if (existingItem) {
      existingItem.quantity += item.quantity;
    } else {
      this.cartItems.push(item);
    }
  }

  /**
   * Incrementar quantidade de um item no carrinho
   * Atualiza localmente e chama backend
   */
  incrementItem(item: any) {
    if (!item.id) return;

    console.log('⬆️ Incrementando item:', item.name);
    const novaQuantidade = item.quantity + 1;

    // Remover item atual do backend
    this.carrinhoService.removerItem(item.id).subscribe({
      next: () => {
        // Readicionar com nova quantidade
        const produtoId = item.produto_id || null;
        const pizzaId = item.pizza_id || null;

        this.carrinhoService.adicionarItem({
          produto_id: produtoId,
          produto_personalizado_id: pizzaId,
          quantidade: novaQuantidade
        }).subscribe({
          next: (resposta) => {
            console.log('✅ Item atualizado com sucesso');
            // Atualizar apenas o item local sem recarregar todo o carrinho
            item.quantity = resposta.quantidade;
            item.preco_total = resposta.quantidade * item.preco_unitario;
          },
          error: (error) => {
            console.error('❌ Erro ao readicionar item:', error);
          }
        });
      },
      error: (error) => {
        console.error('❌ Erro ao remover item:', error);
      }
    });
  }

  /**
   * Decrementar quantidade de um item no carrinho
   * Remove item se quantidade for 1
   */
  decrementItem(item: any) {
    if (!item.id) return;

    console.log('⬇️ Decrementando item:', item.nome);

    if (item.quantidade > 1) {
      const novaQuantidade = item.quantidade - 1;

      // Remover item atual do backend
      this.carrinhoService.removerItem(item.id).subscribe({
        next: () => {
          // Readicionar com nova quantidade
          const produtoId = item.produto_id || null;
          const pizzaId = item.pizza_id || null;

          this.carrinhoService.adicionarItem({
            produto_id: produtoId,
            produto_personalizado_id: pizzaId,
            quantidade: novaQuantidade
          }).subscribe({
            next: (resposta) => {
              console.log('✅ Item atualizado com sucesso');
              // Atualizar apenas o item local sem recarregar todo o carrinho
              item.quantity = resposta.quantidade;
              item.preco_total = resposta.quantidade * item.preco_unitario;
            },
            error: (error) => {
              console.error('❌ Erro ao readicionar item:', error);
            }
          });
        },
        error: (error) => {
          console.error('❌ Erro ao remover item:', error);
        }
      });
    } else {
      // Se quantidade é 1, apenas remove
      this.removeItem(item);
    }
  }

  /**
   * Remover item do carrinho
   */
  removeItem(item: any) {
    if (!item.id) return;

    console.log('🗑️ Removendo item:', item.name);
    this.carrinhoService.removerItem(item.id).subscribe({
      next: () => {
        console.log('✅ Item removido com sucesso');
        // Remover do array local sem recarregar
        const index = this.cartItems.indexOf(item);
        if (index > -1) {
          this.cartItems.splice(index, 1);
        }
      },
      error: (error) => {
        console.error('❌ Erro ao remover item:', error);
      }
    });
  }

  subtotal() {
    let itemTotal = 0;

    for (let item of this.cartItems) {
      // Usar preco_total do backend (já é quantidade * preco_unitario)
      itemTotal += item.quantity * item.price || 0;
    }

    return itemTotal;
  }

  total() {
    return this.subtotal() + this.deliveryFee;
  }

  /**
   * Finalizar pedido - criar pedido no backend e limpar carrinho
   */
  finalizarPedido(): void {
    // Validar carrinho sincronizado com backend
    if (this.cartItems.length === 0) {
      alert('Carrinho vazio! Adicione itens antes de finalizar.');
      this.carregarCarrinho(); // Recarregar para garantir sincronização
      return;
    }

    if (!this.authService.isLoggedIn()) {
      alert('Você precisa estar logado para finalizar um pedido!');
      return;
    }

    this.isLoading = true;
    console.log('🛒 Finalizando pedido...');
    const token = this.authService.getToken();
    console.log('🔐 CartComponent: Token disponível?', !!token);
    console.log('🔐 CartComponent: Token value:', token ? token.substring(0, 20) + '...' : 'NO TOKEN');
    console.log('📦 CartComponent: Items no carrinho:', this.cartItems.length);

    // Obter email do cliente logado
    this.authService.getClienteInfo().subscribe({
      next: (cliente) => {
        const pedidoData = {
          descricao: `Pedido com ${this.cartItems.length} item(ns)`,
          email: cliente.email
        };

        console.log('📤 Enviando pedido com email:', cliente.email);

        this.pedidosService.finalizarPedido(pedidoData).subscribe({
          next: (pedido) => {
            console.log('✅ Pedido finalizado com sucesso:', pedido);
            // Limpar carrinho local
            this.cartItems = [];
            this.isLoading = false;
            // Fechar carrinho
            this.open.set(false);
            // Emitir evento para atualizar a página de pedidos
            this.pedidoFinalizado.emit();
            alert('Pedido finalizado com sucesso!');
          },
          error: (error) => {
            console.error('❌ Erro ao finalizar pedido:', error);
            console.error('Status:', error.status);
            console.error('Message:', error.message);
            console.error('URL:', error.url);
            this.isLoading = false;
            alert('Erro ao finalizar pedido. Tente novamente.');
          }
        });
      },
      error: (error) => {
        console.error('❌ Erro ao obter dados do cliente:', error);
        this.isLoading = false;
        alert('Erro ao obter dados do cliente. Tente novamente.');
      }
    });
  }
}


