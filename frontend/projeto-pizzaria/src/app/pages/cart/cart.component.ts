import { Component, Input, WritableSignal, Output, EventEmitter, OnInit, ViewChild, ElementRef } from '@angular/core';
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
  @ViewChild('itemsContainer') itemsContainer!: ElementRef<HTMLElement>;

  // When non-null, carregarCarrinho will restore this scrollTop after reload
  private pendingScrollTop: number | null = null;

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
        // Restaurar posição de scroll se houver uma pendência
        if (this.pendingScrollTop !== null) {
          // esperar próxima microtask para garantir que DOM foi atualizado
          setTimeout(() => {
            try {
              if (this.itemsContainer && this.itemsContainer.nativeElement) {
                this.itemsContainer.nativeElement.scrollTop = this.pendingScrollTop as number;
              }
            } catch (err) {
              console.warn('Não foi possível restaurar scroll do carrinho:', err);
            } finally {
              this.pendingScrollTop = null;
            }
          }, 0);
        }
      },
      error: (error) => {
        console.error('❌ Erro ao carregar carrinho:', error);
        this.cartItems = [];
      }
    });
  }

  /**
   * Incrementar quantidade de um item no carrinho
   * Atualiza localmente e chama backend
   */
  incrementItem(item: any) {
    if (!item.id) return;

    console.log('⬆️ Incrementando item (optimista):', item.nome);
    const novaQuantidade = item.quantidade + 1;

    // Atualização otimista local (mantém ordem)
    const idx = this.cartItems.findIndex((ci: any) => ci.id === item.id || (ci.produto_id === item.produto_id && ci.pizza_id === item.pizza_id));
    if (idx !== -1) {
      // atualizar localmente imediatamente
      const local = this.cartItems[idx];
      local.quantidade = novaQuantidade;
      if (local.preco_unitario != null) {
        local.preco_total = local.preco_unitario * novaQuantidade;
      }
    }

    // Requisitar ao backend para persistir (+1)
    const produtoId = item.produto_id || null;
    const pizzaId = item.pizza_id || null;

    this.carrinhoService.adicionarItem({
      produto_id: produtoId,
      produto_personalizado_id: pizzaId,
      quantidade: 1
    }).subscribe({
      next: (resp: any) => {
        // sincronizar campos retornados (id/quantidade)
        try {
          const idx2 = this.cartItems.findIndex((ci: any) => ci.id === item.id || (ci.produto_id === item.produto_id && ci.pizza_id === item.pizza_id));
          if (idx2 !== -1) {
            this.cartItems[idx2].quantidade = resp.quantidade;
            // atualizar id caso tenha mudado
            this.cartItems[idx2].id = resp.id;
            if (this.cartItems[idx2].preco_unitario != null) {
              this.cartItems[idx2].preco_total = this.cartItems[idx2].preco_unitario * resp.quantidade;
            }
          }
        } catch (err) {
          console.warn('Erro ao sincronizar item após adicionar:', err);
        }
      },
      error: (error) => {
        console.error('❌ Erro ao adicionar item (+1):', error);
        // Em caso de erro, recarregar para garantir consistência
        this.carregarCarrinho();
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

      console.log('⬇️ Decrementando item (optimista):', item.nome);

      // Atualização otimista local (mantém ordem)
      const idx = this.cartItems.findIndex((ci: any) => ci.id === item.id || (ci.produto_id === item.produto_id && ci.pizza_id === item.pizza_id));
      if (idx !== -1) {
        const local = this.cartItems[idx];
        local.quantidade = novaQuantidade;
        if (local.preco_unitario != null) {
          local.preco_total = local.preco_unitario * novaQuantidade;
        }
      }

      // Para persistir a nova quantidade, removemos e readicionamos no backend (como antes)
      // mas NÃO recarregamos a lista ao final — mantemos a ordem local.
      this.carrinhoService.removerItem(item.id).subscribe({
        next: () => {
          const produtoId = item.produto_id || null;
          const pizzaId = item.pizza_id || null;
          this.carrinhoService.adicionarItem({
            produto_id: produtoId,
            produto_personalizado_id: pizzaId,
            quantidade: novaQuantidade
          }).subscribe({
            next: (resp: any) => {
              // atualizar id/quantidade local conforme resposta
              const idx2 = this.cartItems.findIndex((ci: any) => ci.produto_id === produtoId && ci.pizza_id === pizzaId);
              if (idx2 !== -1) {
                this.cartItems[idx2].id = resp.id;
                this.cartItems[idx2].quantidade = resp.quantidade;
                if (this.cartItems[idx2].preco_unitario != null) {
                  this.cartItems[idx2].preco_total = this.cartItems[idx2].preco_unitario * resp.quantidade;
                }
              }
            },
            error: (error) => {
              console.error('❌ Erro ao re-adicionar item (decrement):', error);
              this.carregarCarrinho();
            }
          });
        },
        error: (error) => {
          console.error('❌ Erro ao remover item (decrement):', error);
          this.carregarCarrinho();
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

    console.log('🗑️ Removendo item:', item.nome);
    // Atualização otimista local: remover da lista e manter scroll
    const idx = this.cartItems.findIndex((ci: any) => ci.id === item.id || (ci.produto_id === item.produto_id && ci.pizza_id === item.pizza_id));
    if (idx !== -1) {
      // capturar scroll antes da remoção
      try { this.pendingScrollTop = this.itemsContainer?.nativeElement?.scrollTop ?? null; } catch { this.pendingScrollTop = null; }
      this.cartItems.splice(idx, 1);
    }

    this.carrinhoService.removerItem(item.id).subscribe({
      next: () => {
        console.log('✅ Item removido do backend com sucesso');
        // não recarregamos inteira a lista para evitar reordenação
        // atualizar contagem já é feita pelo serviço
      },
      error: (error) => {
        console.error('❌ Erro ao remover item no backend:', error);
        // fallback: recarregar para garantir consistência
        this.carregarCarrinho();
      }
    });
  }

  subtotal() {
    let itemTotal = 0;

    for (let item of this.cartItems) {
      // Usar preco_total do backend (já é quantidade * preco_unitario)
      itemTotal += item.preco_total || 0;
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


