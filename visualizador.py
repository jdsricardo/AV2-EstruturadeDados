"""
Classe para visualizar o grafo de emergência médica
Utiliza matplotlib e networkx para criar uma representação visual mais realista
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import FancyBboxPatch
import random

class VisualizadorGrafo:
    def __init__(self, grafo_emergencia):
        self.grafo = grafo_emergencia
        
    def plotar_grafo(self):
        """Cria e exibe a visualização do grafo com layout mais realista"""
        # Criar grafo NetworkX
        G = nx.Graph()
        
        # Adicionar nós com posições das coordenadas
        pos = {}
        for nome, (x, y) in self.grafo.coordenadas.items():
            G.add_node(nome, tipo=self.grafo.tipos[nome])
            pos[nome] = (x, y)
        
        # Adicionar arestas com pesos (tempo com trânsito)
        nomes = list(self.grafo.pontos.keys())
        for i, nome1 in enumerate(nomes):
            for j, nome2 in enumerate(nomes):
                if i < j and self.grafo.matriz[i][j] != float('inf'):
                    tempo_atual = self.grafo.get_tempo_com_transito(i, j)
                    G.add_edge(nome1, nome2, weight=tempo_atual)
        
        # Configurar a visualização
        plt.figure(figsize=(14, 10))
        plt.title("🏥 Sistema de Emergência Médica - Rede Hospitalar da Cidade", 
                 fontsize=18, fontweight='bold', pad=30)
        
        # Adicionar fundo simulando uma cidade
        self._adicionar_fundo_cidade()
        
        # Definir cores e tamanhos por tipo de ponto
        cores_nos, tamanhos_nos = self._obter_estilos_nos(G)
        
        # Desenhar nós com estilo aprimorado
        nx.draw_networkx_nodes(G, pos, node_color=cores_nos, 
                              node_size=tamanhos_nos, alpha=0.95,
                              edgecolors='black', linewidths=2)
        
        # Desenhar arestas com estilo curvo e variação de espessura
        self._desenhar_arestas_curvas(G, pos)
        
        # Adicionar rótulos dos nós com estilo melhorado
        self._adicionar_rotulos_nos(G, pos)
        
        # Adicionar rótulos das arestas (tempos)
        self._adicionar_rotulos_arestas(G, pos)
        
        # Adicionar legenda aprimorada
        self._adicionar_legenda()
        
        # Adicionar informações de trânsito
        self._adicionar_info_transito()
        
        # Configurações finais
        plt.axis('off')
        plt.tight_layout()
        
        # Salvar e exibir
        plt.savefig('rede_emergencia.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
        
        print("📊 Mapa da rede hospitalar visualizado e salvo como 'rede_emergencia.png'")
    
    def _adicionar_fundo_cidade(self):
        """Adiciona elementos visuais simulando uma cidade"""
        ax = plt.gca()
        
        # Fundo verde claro simulando área urbana
        ax.set_facecolor('#F0F8F0')
        
        # Adicionar "ruas" principais (linhas mais claras)
        # Ruas horizontais
        for y in range(-4, 5, 2):
            plt.axhline(y=y, color='#E0E0E0', linewidth=3, alpha=0.5, zorder=0)
        
        # Ruas verticais
        for x in range(-5, 6, 2):
            plt.axvline(x=x, color='#E0E0E0', linewidth=3, alpha=0.5, zorder=0)
    
    def _obter_estilos_nos(self, G):
        """Define cores e tamanhos dos nós baseados no tipo"""
        cores = []
        tamanhos = []
        
        for nome in G.nodes():
            tipo = self.grafo.tipos[nome]
            if tipo == "hospital":
                cores.append("#FF4444")  # Vermelho para hospitais
                tamanhos.append(3000)
            elif tipo == "upa":
                cores.append("#44AA44")  # Verde para UPAs
                tamanhos.append(2500)
            else:  # pronto_socorro
                cores.append("#4444FF")  # Azul para pronto socorro
                tamanhos.append(2000)
        
        return cores, tamanhos
    
    def _desenhar_arestas_curvas(self, G, pos):
        """Desenha arestas com curvas realistas e espessuras variadas"""
        for edge in G.edges():
            nome1, nome2 = edge
            x1, y1 = pos[nome1]
            x2, y2 = pos[nome2]
            
            # Calcular espessura baseada na facilidade de acesso
            i = self.grafo.pontos[nome1]
            j = self.grafo.pontos[nome2]
            tempo_base = self.grafo.matriz[i][j]
            tempo_atual = self.grafo.get_tempo_com_transito(i, j)
            
            # Espessura inversamente proporcional ao tempo
            espessura = max(1, 8 - tempo_base / 3)
            
            # Cor baseada no trânsito atual
            fator_transito = tempo_atual / tempo_base
            if fator_transito < 1.2:
                cor = '#2ECC71'  # Verde - trânsito leve
            elif fator_transito < 1.8:
                cor = '#F39C12'  # Laranja - trânsito moderado            else:
                cor = '#E74C3C'  # Vermelho - trânsito pesado
            # Criar curva para a aresta
            self._desenhar_aresta_curva(x1, y1, x2, y2, cor, espessura)
    
    def _desenhar_aresta_curva(self, x1, y1, x2, y2, cor, espessura):
        """Desenha uma aresta simulando ruas da cidade que contornam os prédios"""
        # Calcular pontos intermediários seguindo a grade da cidade
        # As ruas passam nas bordas dos quarteirões, não por cima dos prédios
        
        # Determinar se deve seguir rua horizontal ou vertical primeiro
        dx = x2 - x1
        dy = y2 - y1
        
        # Offset das ruas para não passar por cima dos prédios
        offset_rua = 0.4  # Distância da rua até o centro do quarteirão
        
        # Se a distância for pequena, fazer conexão direta mas deslocada
        if abs(dx) < 1.5 and abs(dy) < 1.5:
            # Criar um pequeno desvio para simular rua
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Deslocar o ponto médio para simular passagem pela rua
            if abs(dx) > abs(dy):
                mid_y += offset_rua if dy >= 0 else -offset_rua
            else:
                mid_x += offset_rua if dx >= 0 else -offset_rua
            
            # Desenhar curva suave passando pelo ponto deslocado
            t = np.linspace(0, 1, 30)
            curve_x = x1 + (mid_x - x1) * 2 * t * (1 - t) + (x2 - x1) * t * t
            curve_y = y1 + (mid_y - y1) * 2 * t * (1 - t) + (y2 - y1) * t * t
            
            plt.plot(curve_x, curve_y, color=cor, linewidth=espessura, 
                    alpha=0.8, solid_capstyle='round')
            return
        
        # Para distâncias maiores, seguir padrão de quarteirões
        # Escolher o caminho que contorna os prédios
        
        # Calcular pontos de rua (deslocados dos centros dos prédios)
        if abs(dx) > abs(dy):
            # Primeiro horizontal, depois vertical
            # Rua horizontal passa acima ou abaixo do prédio de origem
            rua_y1 = y1 + (offset_rua if dy >= 0 else -offset_rua)
            rua_x2 = x2 + (offset_rua if dx >= 0 else -offset_rua)
            
            # Pontos da rota
            ponto1 = (x1, y1)  # Origem (prédio)
            ponto2 = (x1, rua_y1)  # Saída para a rua horizontal
            ponto3 = (rua_x2, rua_y1)  # Esquina (mudança de direção)
            ponto4 = (rua_x2, y2)  # Entrada na rua vertical
            ponto5 = (x2, y2)  # Destino (prédio)
            
        else:
            # Primeiro vertical, depois horizontal  
            # Rua vertical passa à esquerda ou direita do prédio de origem
            rua_x1 = x1 + (offset_rua if dx >= 0 else -offset_rua)
            rua_y2 = y2 + (offset_rua if dy >= 0 else -offset_rua)
            
            # Pontos da rota
            ponto1 = (x1, y1)  # Origem (prédio)
            ponto2 = (rua_x1, y1)  # Saída para a rua vertical
            ponto3 = (rua_x1, rua_y2)  # Esquina (mudança de direção)
            ponto4 = (x2, rua_y2)  # Entrada na rua horizontal
            ponto5 = (x2, y2)  # Destino (prédio)
        
        # Desenhar os segmentos da rota
        pontos = [ponto1, ponto2, ponto3, ponto4, ponto5]
        
        for i in range(len(pontos) - 1):
            x_seg = [pontos[i][0], pontos[i+1][0]]
            y_seg = [pontos[i][1], pontos[i+1][1]]
            
            # Segmentos de acesso aos prédios (mais finos e tracejados)
            if i == 0 or i == len(pontos) - 2:
                plt.plot(x_seg, y_seg, color=cor, linewidth=espessura*0.6, 
                        alpha=0.6, linestyle='--', solid_capstyle='round')
            else:
                # Segmentos da rua principal (espessura normal)
                plt.plot(x_seg, y_seg, color=cor, linewidth=espessura, 
                        alpha=0.8, solid_capstyle='round')
        
        # Adicionar pequenas curvas nas esquinas para suavizar
        curve_radius = 0.15
        esquina = pontos[2]  # Ponto da esquina principal
        
        # Desenhar curva suave na esquina
        if abs(dx) > abs(dy):
            # Curva horizontal para vertical
            if dx > 0 and dy > 0:
                angles = np.linspace(np.pi, 3*np.pi/2, 10)
            elif dx > 0 and dy < 0:
                angles = np.linspace(np.pi/2, np.pi, 10)
            elif dx < 0 and dy > 0:
                angles = np.linspace(3*np.pi/2, 2*np.pi, 10)
            else:
                angles = np.linspace(0, np.pi/2, 10)
        else:
            # Curva vertical para horizontal
            if dy > 0 and dx > 0:
                angles = np.linspace(np.pi, 3*np.pi/2, 10)
            elif dy > 0 and dx < 0:
                angles = np.linspace(3*np.pi/2, 2*np.pi, 10)
            elif dy < 0 and dx > 0:
                angles = np.linspace(np.pi/2, np.pi, 10)
            else:
                angles = np.linspace(0, np.pi/2, 10)
        
        curve_x = esquina[0] + curve_radius * np.cos(angles)
        curve_y = esquina[1] + curve_radius * np.sin(angles)
        
        plt.plot(curve_x, curve_y, color=cor, linewidth=espessura, 
                alpha=0.8, solid_capstyle='round')
    
    def _adicionar_rotulos_nos(self, G, pos):
        """Adiciona rótulos dos nós com formatação melhorada"""
        for nome, (x, y) in pos.items():
            # Texto com fundo branco semi-transparente
            plt.annotate(nome, (x, y), xytext=(0, -25), 
                        textcoords='offset points',
                        ha='center', va='top',
                        fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor='white', alpha=0.8),
                        color='black')
    
    def _adicionar_rotulos_arestas(self, G, pos):
        """Adiciona rótulos das arestas mostrando tempos"""
        for edge in G.edges():
            nome1, nome2 = edge
            x1, y1 = pos[nome1]
            x2, y2 = pos[nome2]
            
            # Posição no meio da aresta
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            
            # Obter tempo atual
            i = self.grafo.pontos[nome1]
            j = self.grafo.pontos[nome2]
            tempo_atual = self.grafo.get_tempo_com_transito(i, j)
            
            # Texto do tempo
            plt.annotate(f'{tempo_atual:.0f}min', (mx, my),
                        ha='center', va='center',
                        fontsize=8, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.2',
                                facecolor='yellow', alpha=0.8),                        color='black')
    
    def _adicionar_legenda(self):
        """Adiciona legenda detalhada"""
        from matplotlib.lines import Line2D
        
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444', 
                   markersize=12, label='🏥 Hospital'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#44AA44', 
                   markersize=12, label='🚑 UPA'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#4444FF', 
                   markersize=12, label='⛑️ Pronto Socorro'),
            Line2D([0], [0], color='#2ECC71', linewidth=4, label='🟢 Trânsito Leve'),
            Line2D([0], [0], color='#F39C12', linewidth=4, label='🟡 Trânsito Moderado'),
            Line2D([0], [0], color='#E74C3C', linewidth=4, label='🔴 Trânsito Pesado')
        ]
        
        plt.legend(handles=legend_elements, loc='upper left', 
                  bbox_to_anchor=(0.02, 0.98), fontsize=10)
    
    def _adicionar_info_transito(self):
        """Adiciona informações sobre o sistema de trânsito"""
        info_text = "🚗 Trânsito Dinâmico Ativo\n📊 Tempos atualizados em tempo real"
        plt.figtext(0.02, 0.02, info_text, fontsize=9,
                   bbox=dict(boxstyle='round,pad=0.5',
                           facecolor='lightblue', alpha=0.8))
    
    def plotar_rota(self, rota, tempo_total):
        """Destaca uma rota específica no grafo"""
        if not rota or len(rota) < 2:
            print("❌ Rota inválida para visualização")
            return
        
        # Criar grafo NetworkX
        G = nx.Graph()
        pos = {}
        
        # Adicionar todos os nós
        for nome, (x, y) in self.grafo.coordenadas.items():
            G.add_node(nome, tipo=self.grafo.tipos[nome])
            pos[nome] = (x, y)
        
        # Adicionar todas as arestas
        nomes = list(self.grafo.pontos.keys())
        for i, nome1 in enumerate(nomes):
            for j, nome2 in enumerate(nomes):
                if i < j and self.grafo.matriz[i][j] != float('inf'):
                    tempo_atual = self.grafo.get_tempo_com_transito(i, j)
                    G.add_edge(nome1, nome2, weight=tempo_atual)
        
        # Configurar a visualização
        plt.figure(figsize=(14, 10))
        plt.title(f"🚨 Rota de Emergência: {rota[0]} → {rota[-1]} ({tempo_total:.1f} min)", 
                 fontsize=16, fontweight='bold', pad=20)
        
        # Fundo da cidade
        self._adicionar_fundo_cidade()
        
        # Cores dos nós baseadas na rota
        cores_nos = []
        tamanhos_nos = []
        for nome in G.nodes():
            if nome in rota:
                if nome == rota[0]:
                    cores_nos.append("#FF0000")  # Vermelho para origem
                    tamanhos_nos.append(4000)
                elif nome == rota[-1]:
                    cores_nos.append("#00FF00")  # Verde para destino
                    tamanhos_nos.append(4000)
                else:
                    cores_nos.append("#FFA500")  # Laranja para pontos intermediários
                    tamanhos_nos.append(3500)
            else:
                cores_nos.append("#CCCCCC")  # Cinza para outros pontos
                tamanhos_nos.append(2000)
        
        # Desenhar todos os nós
        nx.draw_networkx_nodes(G, pos, node_color=cores_nos, 
                              node_size=tamanhos_nos, alpha=0.9,
                              edgecolors='black', linewidths=2)
        
        # Desenhar todas as arestas (cinza claro)
        for edge in G.edges():
            if edge[0] not in rota or edge[1] not in rota:
                nome1, nome2 = edge
                x1, y1 = pos[nome1]
                x2, y2 = pos[nome2]
                self._desenhar_aresta_curva(x1, y1, x2, y2, '#DDDDDD', 1)
        
        # Destacar arestas da rota
        for i in range(len(rota) - 1):
            nome1, nome2 = rota[i], rota[i + 1]
            x1, y1 = pos[nome1]
            x2, y2 = pos[nome2]
            self._desenhar_aresta_curva(x1, y1, x2, y2, '#FF4444', 6)
        
        # Rótulos dos nós
        self._adicionar_rotulos_nos(G, pos)
        
        # Rótulos das arestas da rota
        for i in range(len(rota) - 1):
            nome1, nome2 = rota[i], rota[i + 1]
            x1, y1 = pos[nome1]
            x2, y2 = pos[nome2]
            
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            
            idx1 = self.grafo.pontos[nome1]
            idx2 = self.grafo.pontos[nome2]
            tempo = self.grafo.get_tempo_com_transito(idx1, idx2)
            
            plt.annotate(f'{tempo:.1f}min', (mx, my),
                        ha='center', va='center',
                        fontsize=10, fontweight='bold',                        bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='red', alpha=0.8),
                        color='white')
        
        # Legenda específica para rota
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF0000', 
                   markersize=12, label='🔴 Origem'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#00FF00', 
                   markersize=12, label='🟢 Destino'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFA500', 
                   markersize=12, label='🟡 Ponto Intermediário'),
            Line2D([0], [0], color='#FF4444', linewidth=4, label='🛣️ Rota Selecionada')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        print(f"🛣️  Rota destacada: {' → '.join(rota)}")
        print(f"⏱️  Tempo total: {tempo_total:.1f} minutos")
