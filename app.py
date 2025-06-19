"""
Sistema de Rotas entre Hospitais - AV2 Estrutura de Dados
Problema real: Otimização de rotas para ambulâncias e transferências médicas
"""

import random
import numpy as np
from mapa_visual import MapaHospitais

class GrafoHospitais:
    def __init__(self):
        # Lista de hospitais
        self.hospitais = ["Hospital Central", "UPA Norte", "Hospital São Lucas", 
                         "UPA Sul", "Hospital Infantil"]
        
        self.num_hospitais = len(self.hospitais)
        
        # Matriz de adjacência com tempos base (minutos)
        self.matriz_base = np.array([
            [0,  12, 18, 15, 22],  # Hospital Central
            [12, 0,  25, 30, 20],  # UPA Norte  
            [18, 25, 0,  14, 8 ],  # Hospital São Lucas
            [15, 30, 14, 0,  16],  # UPA Sul
            [22, 20, 8,  16, 0 ]   # Hospital Infantil
        ])
        
        # Matriz de trânsito (multiplicadores aleatórios)
        self.atualizar_transito()
    
    def atualizar_transito(self):
        """Gera condições de trânsito aleatórias"""
        self.transito = np.ones((self.num_hospitais, self.num_hospitais))
        
        for i in range(self.num_hospitais):
            for j in range(self.num_hospitais):
                if i != j:
                    # Multiplicador entre 0.8 (livre) e 2.2 (congestionado)
                    self.transito[i][j] = random.uniform(0.8, 2.2)
    
    def calcular_tempo(self, origem: int, destino: int) -> float:
        """Calcula tempo atual com trânsito"""
        return self.matriz_base[origem][destino] * self.transito[origem][destino]

def main():
    print("🏥 SISTEMA DE ROTAS ENTRE HOSPITAIS")
    print("="*40)
    
    grafo = GrafoHospitais()
    mapa = MapaHospitais(grafo)
    
    while True:
        print("\n1. Consultar tempo entre hospitais")
        print("2. Visualizar mapa da cidade")
        print("3. Sair")
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == '1':
            print("\nHospitais disponíveis:")
            for i, hospital in enumerate(grafo.hospitais):
                print(f"{i}. {hospital}")
            
            try:
                origem = int(input("\nOrigem: "))
                destino = int(input("Destino: "))
                
                if 0 <= origem < grafo.num_hospitais and 0 <= destino < grafo.num_hospitais:
                    tempo = grafo.calcular_tempo(origem, destino)
                    print(f"\n🚑 Tempo estimado: {tempo:.1f} minutos")
                    print(f"   {grafo.hospitais[origem]} → {grafo.hospitais[destino]}")
                else:
                    print("❌ Números inválidos!")
            except ValueError:
                print("❌ Digite números válidos!")
        
        elif opcao == '2':
            grafo.atualizar_transito()  # Atualiza trânsito antes de mostrar
            mapa.mostrar_mapa()
        
        elif opcao == '3':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()