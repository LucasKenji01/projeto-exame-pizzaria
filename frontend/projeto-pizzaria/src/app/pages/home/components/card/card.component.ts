import { CurrencyPipe } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { TuiButton, TuiIcon } from '@taiga-ui/core';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [TuiButton, TuiIcon, CurrencyPipe, NgIf],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})
export class CardComponent {

  @Input() title: string = '';
  @Input() description: string = '';
  @Input() imageUrl: string = '';
  @Input() logoOverlay?: string | boolean;
  @Input() price: number = 0;
  @Input() id: number = 0;
  @Input() isCustom: boolean = false;

  @Output() deleteCustom = new EventEmitter<number>();

  @Output() addToCart = new EventEmitter<{ id: number; title: string; description: string; price: number; isCustom?: boolean }>();

  getImageUrl(): string {
    return this.imageUrl || '/assets/pizza-padrao.jpg';
  }

  // Retorna true quando a imagem atual é o logo usado para pizzas criadas
  isLogoImage(): boolean {
    const url = this.getImageUrl();
    return !!url && url.includes('/assets/pizzas/logo.svg');
  }

  getLogoUrl(): string | null {
    if (!this.logoOverlay) return null;
    return typeof this.logoOverlay === 'string' ? this.logoOverlay : '/assets/pizzas/logo.svg';
  }

  onAddToCart() {
    console.log('🎯 CardComponent.onAddToCart chamado!', {
      id: this.id,
      title: this.title,
      price: this.price
    });
    this.addToCart.emit({
      id: this.id,
      title: this.title,
      description: this.description,
      price: this.price,
      isCustom: this.isCustom
    });
  }

  onDeleteCustom() {
    if (!this.isCustom) return;
    this.deleteCustom.emit(this.id);
  }
}
