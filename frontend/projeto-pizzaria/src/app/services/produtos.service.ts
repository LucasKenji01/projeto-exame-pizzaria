import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface Produto {
  id: number;
  nome: string;
  descricao?: string;
  preco: number;
  categoria_id?: number;
  imagem_url?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProdutosService {
  private readonly API_URL = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  /**
   * Listar todos os produtos
   */
  listarProdutos(): Observable<Produto[]> {
    console.log('✓ ProdutosService: Fetching GET /produtos');

    return this.http.get<Produto[]>(`${this.API_URL}/produtos`).pipe(
      tap((response) => {
        console.log('✓ ProdutosService: SUCCESS - Recebidos', response.length, 'produtos');
      })
    );
  }

  /**
   * Listar produtos por categoria
   */
  listarProdutosPorCategoria(categoriaId: number): Observable<Produto[]> {
    return this.http.get<Produto[]>(
      `${this.API_URL}/produtos/categoria/${categoriaId}`
    );
  }

  /**
   * Buscar produto por ID
   */
  buscarProdutoPorId(produtoId: number): Observable<Produto> {
    return this.http.get<Produto>(`${this.API_URL}/produtos/${produtoId}`);
  }
}
