"""
Módulo para visualização do mapa de hospitais com ruas e quarteirões realistas
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class MapaHospitais:
    def __init__(self, grafo):
        self.grafo = grafo
        
        # Coordenadas dos hospitais em um mapa de cidade realista
        self.coordenadas = {
            "Hospital Central": (5, 5),
            "UPA Norte": (3, 8),
            "Hospital São Lucas": (8, 7),
            "UPA Sul": (6, 2),
            "Hospital Infantil": (9, 3)
        }
        
        # Definir ruas principais da cidade
        self.ruas = self.criar_ruas()
        
        # Definir quarteirões
        self.quarteiroes = self.criar_quarteiroes()
    
    def criar_ruas(self):
        """Define as ruas principais da cidade"""
        return {
            # Ruas horizontais
            'Av. Principal': [(0, 5), (10, 5)],
            'Rua Norte': [(0, 8), (10, 8)],
            'Rua Sul': [(0, 2), (10, 2)],
            
            # Ruas verticais
            'Av. Central': [(5, 0), (5, 10)],
            'Rua Oeste': [(2, 0), (2, 10)],
            'Rua Leste': [(8, 0), (8, 10)],
            
            # Ruas secundárias
            'Rua Hospital': [(3, 6), (9, 6)],
            'Rua Saúde': [(4, 1), (4, 9)],
            'Rua Emergência': [(6, 1), (6, 9)]
        }
    
    def criar_quarteiroes(self):
        """Define os quarteirões da cidade"""
        return [
            # Quarteirões residenciais
            [(1, 1), (3, 1), (3, 4), (1, 4)],
            [(4, 1), (6, 1), (6, 4), (4, 4)],
            [(7, 1), (9, 1), (9, 4), (7, 4)],
            
            # Quarteirões comerciais
            [(1, 6), (3, 6), (3, 9), (1, 9)],
            [(4, 6), (6, 6), (6, 9), (4, 9)],
            [(7, 6), (9, 6), (9, 9), (7, 9)],
            
            # Parque central
            [(3.5, 4.5), (6.5, 4.5), (6.5, 5.5), (3.5, 5.5)]
        ]
    
    def desenhar_ruas(self, ax):
        """Desenha as ruas no mapa"""
        for nome, coords in self.ruas.items():
            x_coords = [coords[0][0], coords[1][0]]
            y_coords = [coords[0][1], coords[1][1]]
            
            # Cor e espessura baseada no tipo de rua
            if 'Av.' in nome:
                cor = '#444444'  # Cinza escuro para avenidas
                largura = 3
            else:
                cor = '#666666'  # Cinza médio para ruas
                largura = 2
            
            ax.plot(x_coords, y_coords, color=cor, linewidth=largura, alpha=0.8)
            
            # Adicionar nome da rua
            mid_x = (x_coords[0] + x_coords[1]) / 2
            mid_y = (y_coords[0] + y_coords[1]) / 2
            
            # Ajustar posição do texto
            offset_x = 0.2 if coords[0][1] == coords[1][1] else 0
            offset_y = 0.2 if coords[0][0] == coords[1][0] else 0
            
            ax.text(mid_x + offset_x, mid_y + offset_y, nome, 
                   fontsize=8, alpha=0.7, rotation=0 if coords[0][1] == coords[1][1] else 90)
    
    def desenhar_quarteiroes(self, ax):
        """Desenha os quarteirões no mapa"""
        for i, quarteirao in enumerate(self.quarteiroes):
            # Cores diferentes para tipos de quarteirão
            if i < 3:  # Residenciais
                cor = '#E8F5E8'
                alpha = 0.6
            elif i < 6:  # Comerciais
                cor = '#E8E8F5'
                alpha = 0.6
            else:  # Parque
                cor = '#90EE90'
                alpha = 0.8
            
            # Criar polígono do quarteirão
            polygon = patches.Polygon(quarteirao, closed=True, 
                                    facecolor=cor, alpha=alpha, 
                                    edgecolor='black', linewidth=0.5)
            ax.add_patch(polygon)
    
    def desenhar_conexoes(self, ax):
        """Desenha as conexões entre hospitais com cores baseadas no trânsito"""
        for i in range(self.grafo.num_hospitais):
            for j in range(i + 1, self.grafo.num_hospitais):
                hospital1 = self.grafo.hospitais[i]
                hospital2 = self.grafo.hospitais[j]
                
                x1, y1 = self.coordenadas[hospital1]
                x2, y2 = self.coordenadas[hospital2]
                
                # Determinar cor baseada no trânsito
                multiplicador = self.grafo.transito[i][j]
                if multiplicador < 1.2:
                    cor = '#00CC00'  # Verde - trânsito livre
                    alpha = 0.7
                elif multiplicador < 1.8:
                    cor = '#FF8C00'  # Laranja - trânsito moderado
                    alpha = 0.8
                else:
                    cor = '#FF4444'  # Vermelho - congestionamento
                    alpha = 0.9
                
                # Desenhar rota com curvas realistas
                self.desenhar_rota_curva(ax, x1, y1, x2, y2, cor, alpha)                
                # Adicionar tempo no meio da rota
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                tempo = self.grafo.calcular_tempo(i, j)
                ax.text(mid_x, mid_y, f'{tempo:.0f}min', 
                       fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    def desenhar_rota_curva(self, ax, x1, y1, x2, y2, cor, alpha):
        """Desenha uma rota que segue as ruas do mapa"""
        # Pontos intermediários seguindo as ruas principais
        rota_x = []
        rota_y = []
        
        # Sempre começar pelo ponto de origem
        rota_x.append(x1)
        rota_y.append(y1)
        
        # Lógica para seguir ruas: primeiro ir para uma rua principal, depois para o destino
        # Se estão na mesma linha horizontal ou vertical, rota mais direta
        if abs(x1 - x2) < 0.5:  # Mesma coluna aproximadamente
            if y1 < y2:  # Indo para norte
                rota_x.extend([x1, x2])
                rota_y.extend([5, y2])  # Passa pela Av. Principal
            else:  # Indo para sul
                rota_x.extend([x1, x2])
                rota_y.extend([5, y2])  # Passa pela Av. Principal
        elif abs(y1 - y2) < 0.5:  # Mesma linha aproximadamente
            if x1 < x2:  # Indo para leste
                rota_x.extend([5, x2])
                rota_y.extend([y1, y2])  # Passa pela Av. Central
            else:  # Indo para oeste
                rota_x.extend([5, x2])
                rota_y.extend([y1, y2])  # Passa pela Av. Central
        else:
            # Rota em L seguindo as ruas principais
            # Primeiro vai para Av. Central (x=5), depois para a rua do destino
            rota_x.extend([5, 5, x2])
            rota_y.extend([y1, y2, y2])
        
        # Desenhar a rota seguindo os pontos das ruas
        for i in range(len(rota_x) - 1):
            ax.plot([rota_x[i], rota_x[i+1]], [rota_y[i], rota_y[i+1]], 
                   color=cor, linewidth=4, alpha=alpha)
            
            # Adicionar pequenas curvas nos cruzamentos
            if i > 0 and i < len(rota_x) - 2:
                # Círculo pequeno no cruzamento
                circle = patches.Circle((rota_x[i], rota_y[i]), 0.1, 
                                      facecolor=cor, alpha=alpha*0.7)
                ax.add_patch(circle)
    
    def desenhar_hospitais(self, ax):
        """Desenha os hospitais no mapa"""
        for i, hospital in enumerate(self.grafo.hospitais):
            x, y = self.coordenadas[hospital]
            
            # Ícone do hospital
            if 'UPA' in hospital:
                cor = '#FF6B6B'  # Vermelho para UPA
                tamanho = 200
                simbolo = '+'
            else:
                cor = '#4ECDC4'  # Azul para hospitais
                tamanho = 300
                simbolo = 'H'
            
            # Desenhar círculo de fundo
            circle = patches.Circle((x, y), 0.4, facecolor=cor, 
                                  edgecolor='white', linewidth=2, alpha=0.9)
            ax.add_patch(circle)
            
            # Adicionar símbolo
            ax.text(x, y, simbolo, fontsize=16, fontweight='bold', 
                   color='white', ha='center', va='center')
            
            # Nome do hospital
            ax.text(x, y-0.7, hospital, fontsize=10, fontweight='bold',
                   ha='center', va='top',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    def mostrar_mapa(self):
        """Exibe o mapa completo da cidade"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 12))
        
        # Configurar limites do mapa
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        
        # Fundo da cidade
        ax.set_facecolor('#F0F0F0')
        
        # Desenhar elementos do mapa
        self.desenhar_quarteiroes(ax)
        self.desenhar_ruas(ax)
        self.desenhar_conexoes(ax)
        self.desenhar_hospitais(ax)
          # Título e legendas
        ax.set_title('🏥 MAPA DA CIDADE - REDE HOSPITALAR\nCom Trânsito em Tempo Real', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Criar legenda com cores reais
        from matplotlib.lines import Line2D
        
        # Elementos da legenda de trânsito
        legend_elements = [
            Line2D([0], [0], color='#FF4444', lw=4, label='Trânsito Pesado (>1.8x)'),
            Line2D([0], [0], color='#FF8C00', lw=4, label='Trânsito Moderado (1.2-1.8x)'),
            Line2D([0], [0], color='#00CC00', lw=4, label='Trânsito Livre (<1.2x)')
        ]
        
        # Adicionar legenda no canto superior esquerdo
        legend1 = ax.legend(handles=legend_elements, loc='upper left', 
                           bbox_to_anchor=(0.02, 0.98), fontsize=10,
                           title='Condições de Trânsito', title_fontsize=11)
        legend1.get_frame().set_facecolor('white')
        legend1.get_frame().set_alpha(0.9)
        
        # Legenda para hospitais
        legenda_hospitais = """🏥 Hospitais Gerais  🚑 UPAs"""
        ax.text(0.02, 0.15, legenda_hospitais, 
               transform=ax.transAxes,
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9),
               fontsize=10, verticalalignment='top')
        
        # Remover eixos para parecer mais com um mapa
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Adicionar grade sutil
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        plt.show()
