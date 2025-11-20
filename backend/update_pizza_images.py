#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para atualizar as URLs das pizzas de .svg para .jpg
"""

import sys
import os

# Adiciona o diretório do projeto ao path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_path)

from pizzaria_api_pkg.database import SessionLocal
from pizzaria_api_pkg.core_models import Produto

# Mapeamento de nomes de pizzas para nomes de arquivos JPG
pizzas_mapping = {
    'Margherita': 'margherita.jpg',
    'Calabresa': 'calabresa.jpg',
    'Pepperoni': 'pepperoni.jpg',
    'Portuguesa': 'portuguesa.jpg',
    'Quatro Queijos': 'quatro-queijos.jpg',
    'Frango com Catupiry': 'frango-catupiry.jpg',
    'Vegetariana': 'vegetariana.jpg',
    'Bacon': 'bacon.jpg',
    'Presunto e Abacaxi': 'presunto-abacaxi.jpg',
    'Moda da Casa': 'moda-da-casa.jpg',
    'Brigadeiro com Especiarias': 'brigadeiro-especiarias.jpg',
    'Alho e Óleo': 'alho-oleo.jpg',
    'Brócolis com Alho': 'broccolis-alho.jpg',
    'Champignon': 'champignon.jpg',
    'Rúcula e Parmesan': 'rucula-parmesan.jpg',
    'Atum': 'atum.jpg',
    'Linguiça Calabresa': 'linguica-calabresa.jpg',
    'Ovos e Cebola': 'ovos-cebola.jpg',
    'Milho Verde': 'milho-verde.jpg',
    'Camarão': 'camarao.jpg',
    'Chocolate com Morango': 'chocolate-morango.jpg',
    'Banana com Canela': 'banana-canela.jpg',
    'Doce de Leite com Banana': 'doce-leite-banana.jpg',
    'Nutella': 'nutella.jpg',
    'Maçã com Canela': 'maca-canela.jpg'
}

def main():
    print("\n" + "="*60)
    print("🍕 ATUALIZANDO URLs DAS PIZZAS PARA JPG")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        atualizadas = 0
        nao_encontradas = []
        
        for pizza_nome, arquivo in pizzas_mapping.items():
            pizza = db.query(Produto).filter(Produto.nome == pizza_nome).first()
            if pizza:
                antiga_url = pizza.imagem_url
                pizza.imagem_url = f'/assets/pizzas/{arquivo}'
                atualizadas += 1
                print(f"✅ {pizza_nome}")
                print(f"   De: {antiga_url}")
                print(f"   Para: /assets/pizzas/{arquivo}\n")
            else:
                nao_encontradas.append(pizza_nome)
                print(f"⚠️  Pizza '{pizza_nome}' não encontrada no banco\n")
        
        db.commit()
        
        print("="*60)
        print(f"✨ {atualizadas} pizzas atualizadas com sucesso!")
        if nao_encontradas:
            print(f"⚠️  {len(nao_encontradas)} pizzas não encontradas")
        print("="*60 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao atualizar: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
