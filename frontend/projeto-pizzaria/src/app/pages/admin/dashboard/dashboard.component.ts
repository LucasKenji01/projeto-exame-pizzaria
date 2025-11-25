import { Component } from '@angular/core';
import { TuiAxes } from '@taiga-ui/addon-charts/components/axes';
import { TuiBarChart } from '@taiga-ui/addon-charts/components/bar-chart';
import { tuiCeil } from '@taiga-ui/cdk';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  imports: [TuiAxes, TuiBarChart]
})
export class AdminDashboardComponent {

  protected value = [
    // fallback inicial (será sobrescrito pela chamada ao backend)
    [3660, 8281, 1069, 9034, 5797, 6918, 8495, 3234, 6204, 1392, 2088, 8637],
  ];

  protected readonly labelsX = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  protected labelsY: string[] = [];
  protected chartMax = 100;

  protected getHeight(max: number): number {
    return (max / tuiCeil(max, -3)) * 100;
  }

  private readonly API_URL = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.http.get<number[]>(`${this.API_URL}/relatorios/vendas-mes`).subscribe({
      next: (data) => {
        if (Array.isArray(data) && data.length === 12) {
          this.value = [data];
          const maxVal = Math.max(...data.map(d => Number(d) || 0));
          const suggested = Math.max(1, maxVal);
          this.chartMax = Math.max(10, tuiCeil(suggested, -3));
          this.labelsY = ['0', String(this.chartMax)];
        } else {
          console.warn('Relatório mensal retornou formato inesperado:', data);
        }
      },
      error: (err) => {
        console.error('Erro ao carregar relatório mensal:', err);
      }
    });
  }

}
