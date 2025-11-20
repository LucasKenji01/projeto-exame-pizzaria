import { registerLocaleData } from '@angular/common';
import { Component, LOCALE_ID } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TuiRoot } from '@taiga-ui/core';
import localePt from '@angular/common/locales/pt';

registerLocaleData(localePt)

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    TuiRoot,
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'pt' }
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

}
