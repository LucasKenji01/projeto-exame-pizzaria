import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PizzaOut {
  id: number;
  nome: string;
  preco_base: number;
}

@Injectable({
  providedIn: 'root'
})
export class PizzasService {
  private readonly API_URL = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  criarPizza(nome: string, preco_base: number): Observable<PizzaOut> {
    return this.http.post<PizzaOut>(`${this.API_URL}/pizzas/`, { nome, preco_base });
  }

  listarMinhas(): Observable<PizzaOut[]> {
    return this.http.get<PizzaOut[]>(`${this.API_URL}/pizzas/me`);
  }

  excluirPizza(pizzaId: number) {
    return this.http.delete(`${this.API_URL}/pizzas/${pizzaId}`);
  }
}
