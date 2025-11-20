import { CurrencyPipe } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { TuiButton, TuiIcon } from '@taiga-ui/core';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [TuiButton, TuiIcon, CurrencyPipe],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})
export class CardComponent {

  @Input() title: string = '';
  @Input() description: string = '';
  @Input() imageUrl: string = '';
  @Input() price: number = 0;

  @Output() addToCart = new EventEmitter<{ title: string; description: string; price: number }>();

  getImageUrl(): string {
    return this.imageUrl || '/assets/pizza-padrao.jpg';
  }

  onAddToCart() {
    this.addToCart.emit({
      title: this.title,
      description: this.description,
      price: this.price
    });
  }
}
