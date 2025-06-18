"""
Classe para representar o grafo de emergência médica
Utiliza matriz de adjacência para armazenar os tempos entre pontos
Inclui sistema de trânsito dinâmico e coordenadas realistas
"""

import random
import math

class GrafoEmergencia:
    def __init__(self):
        self.pontos = {}      # Dicionário: nome -> índice
        self.tipos = {}       # Dicionário: nome -> tipo do ponto
        self.coordenadas = {} # Dicionário: nome -> (x, y)
        self.matriz = []      # Matriz de adjacência (tempos base)
        self.contador = 0     # Contador de pontos adicionados
        self.seed_transito = random.randint(1, 1000)  # Seed para consistência na sessão
    
    def adicionar_ponto(self, nome, tipo_ponto, coordenadas=(0, 0)):
        """Adiciona um novo ponto médico ao grafo com coordenadas"""
        if nome not in self.pontos:
            # Adicionar o ponto ao dicionário
            self.pontos[nome] = self.contador
            self.tipos[nome] = tipo_ponto
            self.coordenadas[nome] = coordenadas
            self.contador += 1
            
            # Expandir a matriz de adjacência
            # Adicionar nova linha
            self.matriz.append([float('inf')] * self.contador)
            
            # Adicionar nova coluna a todas as linhas existentes
            for i in range(len(self.matriz) - 1):
                self.matriz[i].append(float('inf'))
            
            # Distância de um ponto para ele mesmo é 0
            indice = self.pontos[nome]
            self.matriz[indice][indice] = 0
            
            emoji = self.get_emoji_tipo(tipo_ponto)
            print(f"✅ Ponto adicionado: {emoji} {nome} ({tipo_ponto})")
    
    def adicionar_rota(self, origem, destino, tempo_base=None):
        """
        Adiciona uma rota bidirecional entre dois pontos
        Se tempo_base não for fornecido, calcula automaticamente baseado na distância
        """
        if origem in self.pontos and destino in self.pontos:
            i = self.pontos[origem]
            j = self.pontos[destino]
            
            # Se tempo não foi fornecido, calcular baseado na distância
            if tempo_base is None:
                distancia = self.calcular_distancia_euclidiana(origem, destino)
                tempo_base = self.calcular_tempo_por_distancia(distancia)
            
            # Verificar se o tempo é lógico baseado na distância
            distancia = self.calcular_distancia_euclidiana(origem, destino)
            tempo_sugerido = self.calcular_tempo_por_distancia(distancia)
            
            # Usar o tempo base fornecido, mas ajustar se necessário
            tempo_final = max(tempo_base, tempo_sugerido * 0.8)
            
            # Rota bidirecional (grafo não direcionado)
            self.matriz[i][j] = tempo_final
            self.matriz[j][i] = tempo_final
            
            print(f"🛣️  Rota adicionada: {origem} ↔ {destino} ({tempo_final:.1f} min base)")
    
    def calcular_distancia_euclidiana(self, ponto1, ponto2):
        """Calcula a distância euclidiana entre dois pontos"""
        x1, y1 = self.coordenadas[ponto1]
        x2, y2 = self.coordenadas[ponto2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def calcular_tempo_por_distancia(self, distancia):
        """
        Converte distância para tempo aproximado
        Assume velocidade média de 30 km/h em área urbana
        1 unidade de coordenada = ~2 km
        """
        distancia_km = distancia * 2
        velocidade_media = 30  # km/h
        tempo_horas = distancia_km / velocidade_media
        tempo_minutos = tempo_horas * 60
        return max(3, tempo_minutos)  # Mínimo de 3 minutos
    
    def get_tempo_com_transito(self, i, j):
        """
        Calcula o tempo atual considerando o trânsito dinâmico
        Usa uma seed fixa para manter consistência durante a sessão
        """
        if self.matriz[i][j] == float('inf'):
            return float('inf')
        
        # Usar seed baseada na posição na matriz para consistência
        random.seed(self.seed_transito + i * 10 + j)
        
        tempo_base = self.matriz[i][j]
        
        # Fator de trânsito: varia entre 0.9 (tráfego leve) e 2.5 (trânsito pesado)
        fator_transito = random.uniform(0.9, 2.5)
        
        # Resetar seed para não afetar outras operações
        random.seed()
        
        return tempo_base * fator_transito
    
    def get_emoji_tipo(self, tipo):
        """Retorna emoji correspondente ao tipo do ponto"""
        emojis = {
            "hospital": "🏥",
            "upa": "🚑",
            "pronto_socorro": "⛑️"
        }
        return emojis.get(tipo, "🏢")
    
    def exibir_pontos(self):
        """Exibe todos os pontos cadastrados com coordenadas"""
        for nome, tipo_ponto in self.tipos.items():
            emoji = self.get_emoji_tipo(tipo_ponto)
            x, y = self.coordenadas[nome]
            print(f"  {emoji} {nome:20} | Tipo: {tipo_ponto:15} | Coord: ({x:+3}, {y:+3})")
    
    def exibir_matriz(self):
        """Exibe a matriz de adjacência (tempos base) de forma organizada"""
        nomes = list(self.pontos.keys())
        
        print("\n🕐 TEMPOS BASE (sem trânsito):")
        self._imprimir_matriz(nomes, lambda i, j: self.matriz[i][j])
    
    def exibir_matriz_com_transito(self):
        """Exibe a matriz com os tempos atuais (incluindo trânsito)"""
        nomes = list(self.pontos.keys())
        
        print("\n🚗 TEMPOS ATUAIS (com trânsito):")
        self._imprimir_matriz(nomes, lambda i, j: self.get_tempo_com_transito(i, j))
    
    def _imprimir_matriz(self, nomes, func_tempo):
        """Método auxiliar para imprimir matrizes"""
        # Cabeçalho
        print("     ", end="")
        for nome in nomes:
            print(f"{nome[:10]:>10}", end=" ")
        print()
        
        # Linhas da matriz
        for i, nome_linha in enumerate(nomes):
            print(f"{nome_linha[:10]:>10}", end=" ")
            for j in range(len(nomes)):
                valor = func_tempo(i, j)
                if valor == float('inf'):
                    print(f"{'∞':>10}", end=" ")
                else:
                    print(f"{valor:>10.1f}", end=" ")
            print()
    
    def encontrar_rota_mais_rapida(self, origem, destino):
        """
        Usa algoritmo de Dijkstra para encontrar a rota mais rápida
        Considera trânsito atual
        Retorna: (caminho, tempo_total) ou (None, None) se não houver rota
        """
        if origem not in self.pontos or destino not in self.pontos:
            return None, None
        
        inicio = self.pontos[origem]
        fim = self.pontos[destino]
        n = len(self.pontos)
        
        # Inicialização do algoritmo de Dijkstra
        distancias = [float('inf')] * n
        anterior = [-1] * n
        visitados = [False] * n
        
        distancias[inicio] = 0
        
        # Algoritmo de Dijkstra
        for _ in range(n):
            # Encontrar o vértice não visitado com menor distância
            u = -1
            for v in range(n):
                if not visitados[v] and (u == -1 or distancias[v] < distancias[u]):
                    u = v
            
            if distancias[u] == float('inf'):
                break
            
            visitados[u] = True
            
            # Atualizar distâncias dos vizinhos
            for v in range(n):
                if not visitados[v]:
                    tempo_atual = self.get_tempo_com_transito(u, v)
                    if (tempo_atual != float('inf') and
                        distancias[u] + tempo_atual < distancias[v]):
                        
                        distancias[v] = distancias[u] + tempo_atual
                        anterior[v] = u
        
        # Reconstruir o caminho
        if distancias[fim] == float('inf'):
            return None, None
        
        caminho = []
        atual = fim
        while atual != -1:
            # Encontrar o nome do ponto pelo índice
            for nome, indice in self.pontos.items():
                if indice == atual:
                    caminho.append(nome)
                    break
            atual = anterior[atual]
        
        caminho.reverse()
        return caminho, distancias[fim]
