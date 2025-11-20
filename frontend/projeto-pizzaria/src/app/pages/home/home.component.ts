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

  protected customPizzas: { title: string; description: string; imageUrl: string; price: number }[] = [];

  logged: boolean = false;
  isLoading: boolean = false;
  salgadas: Produto[] = [];
  doces: Produto[] = [];
  allPizzas: { title: string; description: string; imageUrl: string; price: number }[] = [];

  constructor(
    private authService: AuthService,
    private produtosService: ProdutosService,
    private router: Router
  ) {}

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

    this.allPizzas = [];
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
        imageUrl: 'assets/pizza-calabresa.jpg',
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
    return this.cartComponent.cartItems.reduce((total, item) => total + (item.quantity || 0), 0);
  }

  onAddToCart(item: { title: string; description: string; price: number }) {
    this.cartComponent.addItem({
      name: item.title,
      description: item.description,
      quantity: 1,
      price: item.price
    });
  }

  public onCreatePizza(pizzaName: string, ingredients: string[]): void {
    const newPizza = {
      title: pizzaName,
      description: 'Ingredientes: ' + ingredients.join(', '),
      imageUrl: 'assets/pizza-calabresa.jpg', // Usar imagem padrão
      price: 60.00
    };

    this.customPizzas.push(newPizza);
    this.openCreatePizza.set(false);
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
