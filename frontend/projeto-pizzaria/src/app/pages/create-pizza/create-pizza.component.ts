import { Component, inject, Input, Output, EventEmitter, WritableSignal } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { TuiDialogService, TuiPopup, TuiButton, TuiTextfield } from '@taiga-ui/core';
import { TUI_CONFIRM, TuiChip, TuiDrawer, TuiBadge } from "@taiga-ui/kit";
import { TuiItemGroup } from '@taiga-ui/layout';
import { TUI_FALSE_HANDLER } from '@taiga-ui/cdk';
import { filter } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { NgForOf, NgIf } from '@angular/common';

@Component({
  selector: 'app-create-pizza',
  imports: [NgForOf, ReactiveFormsModule, TuiDrawer, TuiPopup, TuiButton, TuiTextfield, TuiChip, TuiItemGroup, FormsModule, TuiBadge, NgIf],
  templateUrl: './create-pizza.component.html',
  styleUrl: './create-pizza.component.css'
})
export class CreatePizzaComponent {
  @Input() openCreatePizza!: WritableSignal<boolean>;
  @Output() pizzaCreated = new EventEmitter<{ name: string; ingredients: string[] }>();

  protected readonly dialogs = inject(TuiDialogService);
  protected readonly control = new FormControl('Some value');

  public pizzaName: string = '';

  public isFormValid(): boolean {
    return this.pizzaName.trim().length > 0 && this.selectedIngredients.length >= 2;
  }

  protected readonly ingredients = [
    "Abacaxi",
    "Alcachofra",
    "Alho poró",
    "Atum",
    "Azeitona preta",
    "Azeitona verde",
    "Bacon",
    "Banana",
    "Brócolis",
    "Calabresa",
    "Camarão",
    "Carne seca",
    "Catupiry",
    "Cebola caramelizada",
    "Cebola roxa",
    "Champignon",
    "Chocolate",
    "Escarola",
    "Frango desfiado",
    "Gorgonzola",
    "Jalapeño",
    "Lombo canadense",
    "Manjericão",
    "Milho verde",
    "Mussarela de búfala",
    "Mussarela",
    "Ovo cozido",
    "Palmito",
    "Parmesão",
    "Peito de peru",
    "Pepperoni",
    "Pimenta calabresa",
    "Pimentão amarelo",
    "Pimentão verde",
    "Pimentão vermelho",
    "Provolone",
    "Presunto",
    "Rúcula",
    "Salame italiano",
    "Tomate cereja"
  ];

  protected checked = this.ingredients.map(TUI_FALSE_HANDLER);

  public selectedIngredients: string[] = [];

  public gatherSelectedIngredients(): string[] {
    this.selectedIngredients = [];

    this.checked.forEach((isChecked, index) => {
      if (isChecked) {
        const ingredient = this.ingredients[index];
        if (ingredient) {
          this.selectedIngredients.push(ingredient);
        }
      }
    });

    return this.selectedIngredients;
  }

  public createPizza(): void {
    if (this.isFormValid()) {
      this.pizzaCreated.emit({
        name: this.pizzaName,
        ingredients: [...this.selectedIngredients]
      });

      this.pizzaName = '';
      this.checked = this.ingredients.map(TUI_FALSE_HANDLER);
      this.selectedIngredients = [];
    }
  }

  public onClose(): void {
    if (this.control.pristine) {
        this.openCreatePizza.set(false);

        return;
    }

    this.dialogs
      .open(TUI_CONFIRM, {
          label: 'Cancel editing form?',
          size: 's',
          data: {
              content: 'You have unsaved changes that will be lost',
          },
      })
      .pipe(filter(Boolean))
      .subscribe(() => {
          this.openCreatePizza.set(false);
          this.control.reset('Some value');
      });
  }
}
