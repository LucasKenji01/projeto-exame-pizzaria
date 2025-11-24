import { Component, signal, ViewChild, OnInit, OnDestroy } from '@angular/core';
import { TuiButton, TuiDataListComponent, TuiDropdown } from '@taiga-ui/core';
import { TuiPush, TuiCarousel, TuiDrawer, TuiBadgedContentComponent, TuiBadgeNotification, TuiAvatar, TuiBadge } from '@taiga-ui/kit';
import { RouterLink, Router } from "@angular/router";
import { CardComponent } from './components/card/card.component';
import { CommonModule, NgFor } from '@angular/common';
import { CartComponent } from "../cart/cart.component";
import { CreatePizzaComponent } from "../create-pizza/create-pizza.component";
import { AuthService } from '../../services/auth.service';
import { ProdutosService, Produto } from '../../services/produtos.service';
import { PizzasService } from '../../services/pizzas.service';
import { CarrinhoService } from '../../services/carrinho.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-home',
  imports: [CommonModule, TuiPush, TuiButton, RouterLink, TuiCarousel, CardComponent, CartComponent, CreatePizzaComponent, TuiBadgedContentComponent, TuiBadgeNotification, TuiAvatar, TuiDropdown, NgFor],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit, OnDestroy {
  @ViewChild(CartComponent) cartComponent!: CartComponent;

  protected index1 = 0;
  protected index2 = 0;
  protected index3 = 0;
  protected index4 = 0;

  private authSubscription?: Subscription;
  private produtosSubscription?: Subscription;

  protected items1: any[] = [];
  protected items2: any[] = [];
  protected items3: any[] = [];

  protected readonly openCart = signal(false);
  protected readonly openCreatePizza = signal(false);

  protected customPizzas: { id?: number; title: string; description: string; imageUrl: string; price: number }[] = [];

  logged: boolean = false;
  isLoading: boolean = false;
  salgadas: Produto[] = [];
  doces: Produto[] = [];
  allPizzas: { title: string; description: string; imageUrl: string; price: number }[] = [];

  constructor(
    private authService: AuthService,
    private produtosService: ProdutosService,
    private carrinhoService: CarrinhoService,
    private pizzasService: PizzasService,
    private router: Router
  ) { }

  ngOnInit(): void {
    // Verificar se o usuário está logado ao inicializar o componente
    this.logged = this.authService.isLoggedIn();

    // Se inscrever no observable para atualizar quando o estado de login mudar
    this.authSubscription = this.authService.isLoggedIn$.subscribe(
      (isLoggedIn) => {
        this.logged = isLoggedIn;
      }
    );

    // Carregar produtos do banco de dados
    this.carregarProdutos();

    // Carregar pizzas personalizadas do usuário
    this.carregarMinhasPizzas();

    this.allPizzas = [];
  }

  /**
   * Carrega as pizzas personalizadas do usuário e popula `customPizzas`
   */
  carregarMinhasPizzas(): void {
    this.pizzasService.listarMinhas().subscribe({
      next: (pizzas) => {
        this.customPizzas = pizzas.map(p => ({
          id: p.id,
          title: p.nome,
          description: '',
          imageUrl: '/assets/pizzas/logo.svg',
          price: p.preco_base,
          custom: true
        }));
      },
      error: (err) => {
        console.warn('Não foi possível carregar pizzas personalizadas:', err);
        // manter customPizzas como está (pode ter valores locais ainda)
      }
    });
  }

  /**
   * Carregar produtos do banco de dados e distribuir nas seções
   * Distribui todas as 25 pizzas (20 salgadas + 5 doces) entre as 3 seções
   */
  carregarProdutos(): void {
    this.isLoading = true;
    console.log('🍕 HomeComponent: Carregando produtos...');

    this.produtosSubscription = this.produtosService.listarProdutos().subscribe({
      next: (produtos: Produto[]) => {
        console.log('✓ HomeComponent: Produtos carregados:', produtos.length);

        // Separar em salgadas e doces
        this.salgadas = produtos.filter(p => p.categoria_id === 1); // categoria_id 1 = Salgadas
        this.doces = produtos.filter(p => p.categoria_id === 2); // categoria_id 2 = Doces

        console.log(`📊 Salgadas: ${this.salgadas.length}, Doces: ${this.doces.length}`);

        // Distribuir produtos nas 3 seções - TODAS AS 25 PIZZAS
        // Seção 1 "Mais Pedidos": primeiras 9 salgadas
        this.items1 = this.salgadas.slice(0, 9).map(p => ({
          title: p.nome,
          description: p.descricao || '',
          imageUrl: p.imagem_url || '/assets/pizzas/pizza-padrao.jpg',
          price: p.preco,
          id: p.id
        }));

        // Seção 2 "Favoritos": próximas 9 salgadas
        this.items2 = this.salgadas.slice(9, 18).map(p => ({
          title: p.nome,
          description: p.descricao || '',
          imageUrl: p.imagem_url || '/assets/pizzas/pizza-padrao.jpg',
          price: p.preco,
          id: p.id
        }));

        // Seção 3 "Promoções": últimas 2 salgadas + todos os 5 doces
        const promocoes = [
          ...this.salgadas.slice(18, 20).map(p => ({
            title: p.nome,
            description: p.descricao || '',
            imageUrl: p.imagem_url || '/assets/pizzas/pizza-padrao.jpg',
            price: p.preco,
            id: p.id
          })),
          ...this.doces.map(p => ({
            title: p.nome,
            description: p.descricao || '',
            imageUrl: p.imagem_url || '/assets/pizzas/pizza-padrao.jpg',
            price: p.preco,
            id: p.id
          }))
        ];
        this.items3 = promocoes;

        console.log(`✨ Distribuição completa: Seção 1 (${this.items1.length}), Seção 2 (${this.items2.length}), Seção 3 (${this.items3.length})`);

        this.isLoading = false;
      },
      error: (error) => {
        console.error('❌ HomeComponent: Erro ao carregar produtos:', error);
        // Se falhar, carregar valores padrão
        this.carregarProdutosPadrao();
        this.isLoading = false;
      }
    });
  }

  /**
   * Carregar produtos padrão (fallback se API falhar)
   */
  carregarProdutosPadrao(): void {
    const produtosPadrao = [
      {
        title: 'Pizza de Calabresa',
        description: 'Deliciosa pizza de calabresa com borda recheada de catupiry.',
        imageUrl: '/assets/pizzas/logo.svg',
        price: 35.00
      },
    ];

    this.items1 = produtosPadrao;
    this.items2 = produtosPadrao;
    this.items3 = produtosPadrao;
  }

  ngOnDestroy(): void {
    // Limpar as inscrições quando o componente for destruído
    if (this.authSubscription) {
      this.authSubscription.unsubscribe();
    }
    if (this.produtosSubscription) {
      this.produtosSubscription.unsubscribe();
    }
  }

  public getCartItemsCount(): number {
    if (!this.cartComponent || !this.cartComponent.cartItems) {
      return 0;
    }
    // Alguns lugares usam 'quantidade' (backend) e outros podem usar 'quantity' (legacy).
    // Somar com fallback para cobrir ambos os casos.
    return this.cartComponent.cartItems.reduce((total, item) => {
      const q = (item.quantidade ?? item.quantity ?? 0);
      return total + (Number(q) || 0);
    }, 0);
  }

  onAddToCart(item: { id: number; title: string; description: string; price: number; isCustom?: boolean }) {
    console.log('🛒 Adicionando item ao carrinho:', item.title, 'ID:', item.id, 'isCustom:', item.isCustom);

    const payload: any = { quantidade: 1 };
    if (item.isCustom) {
      payload.produto_personalizado_id = item.id;
    } else {
      payload.produto_id = item.id;
    }

    // Adicionar ao backend
    this.carrinhoService.adicionarItem(payload).subscribe({
      next: () => {
        console.log('✅ Item adicionado ao carrinho com sucesso');
        // Recarregar carrinho para atualizar view
        this.cartComponent.carregarCarrinho();
      },
      error: (error) => {
        console.error('❌ Erro ao adicionar item:', error);
        alert('Erro ao adicionar item ao carrinho. Você está logado?');
      }
    });
  }

  public onCreatePizza(pizzaName: string, ingredients: string[]): void {
    const precoBase = 60.0;

    this.pizzasService.criarPizza(pizzaName, precoBase).subscribe({
      next: (created) => {
        const newPizza = {
          id: created.id,
          title: created.nome,
          description: 'Ingredientes: ' + ingredients.join(', '),
          imageUrl: '/assets/pizzas/logo.svg',
          logoOverlay: false,
          price: created.preco_base,
          custom: true
        };

        this.customPizzas.push(newPizza);
        this.openCreatePizza.set(false);
      },
      error: (err) => {
        console.error('Erro ao criar pizza personalizada:', err);
        alert('Não foi possível salvar a pizza personalizada. Verifique se você está logado.');
      }
    });
  }

  public onDeleteCustom(pizzaId: number) {
    if (!confirm('Excluir esta pizza personalizada?')) return;

    this.pizzasService.excluirPizza(pizzaId).subscribe({
      next: () => {
        this.customPizzas = this.customPizzas.filter(p => p.id !== pizzaId);
      },
      error: (err) => {
        console.error('Erro ao excluir pizza personalizada:', err);
        alert('Não foi possível excluir a pizza.');
      }
    });
  }

  // Template helper to safely read logoOverlay from items with unknown shape
  public getLogoOverlay(item: any): any {
    return item && (item as any).logoOverlay;
  }

  /**
   * Fazer logout do usuário
   */
  onLogout(event?: Event): void {
    if (event) {
      event.preventDefault();
    }
    this.authService.logout();
    // Redirecionar para a página home após logout
    this.router.navigate(['/home']);
  }
}
