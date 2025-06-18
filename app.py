"""
Sistema de Emergência Médica - AV2 Estrutura de Dados
Autor: Ricardo José da Silva
Data: 17 de junho de 2025

Sistema que utiliza grafos para encontrar a rota mais rápida
entre pontos de emergência médica na cidade.
"""

from grafo_emergencia import GrafoEmergencia
from visualizador import VisualizadorGrafo
from menu_interativo import MenuInterativo

def main():
    print("=" * 60)
    print("🏥 SISTEMA DE EMERGÊNCIA MÉDICA - REDE HOSPITALAR")
    print("=" * 60)
    
    # Criar o grafo de emergência
    sistema = GrafoEmergencia()
    
    # Inicializar dados do sistema
    inicializar_rede_hospitalar(sistema)
    
    # Criar menu interativo
    menu = MenuInterativo(sistema)
    
    # Executar menu principal
    menu.executar()

def inicializar_rede_hospitalar(sistema):
    """Inicializa a rede hospitalar com dados realistas"""
    print("\n🏗️  Inicializando rede hospitalar...")
    
    # Adicionar pontos médicos estrategicamente distribuídos
    sistema.adicionar_ponto("Hospital Central", "hospital", (0, 0))
    sistema.adicionar_ponto("UPA Norte", "upa", (-2, 3))
    sistema.adicionar_ponto("Hospital São Lucas", "hospital", (4, 2))
    sistema.adicionar_ponto("UPA Sul", "upa", (1, -3))
    sistema.adicionar_ponto("Pronto Socorro 24h", "pronto_socorro", (-3, -1))
    sistema.adicionar_ponto("Hospital Infantil", "hospital", (3, -2))
    sistema.adicionar_ponto("UPA Leste", "upa", (5, 0))
    sistema.adicionar_ponto("Hospital Universitário", "hospital", (-1, 4))
    
    # Definir conexões com tempos base calculados automaticamente
    # Tempos serão calculados baseados na distância euclidiana
    conexoes = [
        ("Hospital Central", "UPA Norte"),
        ("Hospital Central", "Hospital São Lucas"),
        ("Hospital Central", "Pronto Socorro 24h"),
        ("Hospital Central", "UPA Sul"),
        ("Hospital Central", "Hospital Infantil"),
        
        ("UPA Norte", "Hospital Universitário"),
        ("UPA Norte", "Hospital São Lucas"),
        
        ("Hospital São Lucas", "UPA Leste"),
        ("Hospital São Lucas", "Hospital Infantil"),
        ("Hospital São Lucas", "UPA Sul"),
        
        ("UPA Sul", "Hospital Infantil"),
        ("UPA Sul", "Pronto Socorro 24h"),
        
        ("Pronto Socorro 24h", "Hospital Universitário"),
        
        ("Hospital Infantil", "UPA Leste"),
        
        ("UPA Leste", "Hospital Universitário"),
    ]
    
    # Adicionar todas as conexões (tempo será calculado automaticamente)
    for origem, destino in conexoes:
        # Calcular tempo baseado na distância
        distancia = sistema.calcular_distancia_euclidiana(origem, destino)
        tempo_calculado = sistema.calcular_tempo_por_distancia(distancia)
        sistema.adicionar_rota(origem, destino, tempo_calculado)
    
    print("✅ Rede hospitalar inicializada com sucesso!")

if __name__ == "__main__":
    main()