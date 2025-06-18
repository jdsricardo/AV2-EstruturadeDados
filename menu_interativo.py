"""
Menu interativo para o Sistema de Emergência Médica
Permite ao usuário escolher diferentes opções de visualização e consulta
"""

from visualizador import VisualizadorGrafo

class MenuInterativo:
    def __init__(self, grafo_emergencia):
        self.grafo = grafo_emergencia
        self.visualizador = VisualizadorGrafo(grafo_emergencia)
    
    def executar(self):
        """Loop principal do menu interativo"""
        while True:
            self.exibir_menu_principal()
            opcao = input("\n👆 Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.exibir_panorama_geral()
            elif opcao == "2":
                self.consultar_rota_especifica()
            elif opcao == "3":
                self.visualizar_grafo_completo()
            elif opcao == "4":
                self.exibir_informacoes_sistema()
            elif opcao == "5":
                print("\n👋 Encerrando sistema de emergência médica...")
                break
            else:
                print("\n❌ Opção inválida! Tente novamente.")
            
            input("\n⏸️  Pressione ENTER para continuar...")
    
    def exibir_menu_principal(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*60)
        print("🏥 MENU PRINCIPAL - SISTEMA DE EMERGÊNCIA MÉDICA")
        print("="*60)
        print("1️⃣  Panorama Geral da Rede")
        print("2️⃣  Consultar Rota Específica")
        print("3️⃣  Visualizar Grafo Completo")
        print("4️⃣  Informações do Sistema")
        print("5️⃣  Sair")
        print("="*60)
    
    def exibir_panorama_geral(self):
        """Exibe informações gerais sobre toda a rede"""
        print("\n" + "="*50)
        print("📊 PANORAMA GERAL DA REDE HOSPITALAR")
        print("="*50)
        
        # Informações dos pontos
        print("\n📍 PONTOS MÉDICOS CADASTRADOS:")
        self.grafo.exibir_pontos()
        
        # Matriz com trânsito atual
        print("\n📊 TEMPOS DE DESLOCAMENTO ATUAIS (com trânsito):")
        self.grafo.exibir_matriz_com_transito()
        
        # Estatísticas da rede
        self.exibir_estatisticas_rede()
    
    def consultar_rota_especifica(self):
        """Permite ao usuário consultar uma rota específica"""
        print("\n" + "="*50)
        print("🛣️  CONSULTA DE ROTA ESPECÍFICA")
        print("="*50)
        
        # Listar pontos disponíveis
        pontos = list(self.grafo.pontos.keys())
        print("\n📍 Pontos disponíveis:")
        for i, ponto in enumerate(pontos, 1):
            tipo = self.grafo.tipos[ponto]
            emoji = self.grafo.get_emoji_tipo(tipo)
            print(f"  {i:2d}. {emoji} {ponto}")
        
        try:
            # Selecionar origem
            print("\n🔵 Selecione o ponto de ORIGEM:")
            origem_idx = int(input("Digite o número: ")) - 1
            if origem_idx < 0 or origem_idx >= len(pontos):
                print("❌ Índice inválido!")
                return
            origem = pontos[origem_idx]
            
            # Selecionar destino
            print("\n🔴 Selecione o ponto de DESTINO:")
            destino_idx = int(input("Digite o número: ")) - 1
            if destino_idx < 0 or destino_idx >= len(pontos):
                print("❌ Índice inválido!")
                return
            destino = pontos[destino_idx]
            
            if origem == destino:
                print("❌ Origem e destino não podem ser iguais!")
                return
            
            # Buscar rota
            print(f"\n🔍 Buscando rota mais rápida de {origem} para {destino}...")
            rota, tempo_total = self.grafo.encontrar_rota_mais_rapida(origem, destino)
            
            if rota:
                print(f"\n✅ ROTA ENCONTRADA:")
                print(f"🛣️  Caminho: {' → '.join(rota)}")
                print(f"⏱️  Tempo total: {tempo_total:.1f} minutos")
                
                # Perguntar se quer visualizar
                visualizar = input("\n🖼️  Deseja visualizar esta rota? (s/n): ").lower()
                if visualizar == 's':
                    self.visualizador.plotar_rota(rota, tempo_total)
            else:
                print(f"\n❌ Não foi possível encontrar rota entre {origem} e {destino}")
        
        except ValueError:
            print("❌ Por favor, digite um número válido!")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def visualizar_grafo_completo(self):
        """Gera a visualização completa do grafo"""
        print("\n🖼️  Gerando visualização completa do grafo...")
        self.visualizador.plotar_grafo()
    
    def exibir_informacoes_sistema(self):
        """Exibe informações técnicas do sistema"""
        print("\n" + "="*50)
        print("ℹ️  INFORMAÇÕES DO SISTEMA")
        print("="*50)
        
        num_pontos = len(self.grafo.pontos)
        num_conexoes = self.contar_conexoes()
        
        print(f"📊 Total de pontos médicos: {num_pontos}")
        print(f"🛣️  Total de conexões: {num_conexoes}")
        print(f"🧮 Tamanho da matriz: {num_pontos}x{num_pontos}")
        
        # Tipos de pontos
        tipos_count = {}
        for tipo in self.grafo.tipos.values():
            tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
        
        print(f"\n🏢 Distribuição por tipo:")
        for tipo, count in tipos_count.items():
            emoji = self.grafo.get_emoji_tipo(tipo)
            nome_tipo = tipo.replace('_', ' ').title()
            print(f"  {emoji} {nome_tipo}: {count}")
        
        print(f"\n🚗 Sistema de trânsito: Dinâmico (variação aleatória)")
        print(f"🧭 Algoritmo de rota: Dijkstra")
        print(f"📐 Estrutura de dados: Matriz de adjacência")
    
    def exibir_estatisticas_rede(self):
        """Calcula e exibe estatísticas da rede"""
        print(f"\n📈 ESTATÍSTICAS DA REDE:")
        
        # Tempo médio entre pontos conectados
        tempos = []
        for i in range(len(self.grafo.matriz)):
            for j in range(i + 1, len(self.grafo.matriz)):
                if self.grafo.matriz[i][j] != float('inf'):
                    tempos.append(self.grafo.get_tempo_com_transito(i, j))
        
        if tempos:
            tempo_medio = sum(tempos) / len(tempos)
            tempo_min = min(tempos)
            tempo_max = max(tempos)
            
            print(f"  ⏱️  Tempo médio entre pontos: {tempo_medio:.1f} min")
            print(f"  🏃 Conexão mais rápida: {tempo_min:.1f} min")
            print(f"  🐌 Conexão mais lenta: {tempo_max:.1f} min")
        
        # Ponto mais conectado
        conexoes_por_ponto = {}
        pontos_nomes = list(self.grafo.pontos.keys())
        
        for nome, idx in self.grafo.pontos.items():
            conexoes = 0
            for j in range(len(self.grafo.matriz)):
                if idx != j and self.grafo.matriz[idx][j] != float('inf'):
                    conexoes += 1
            conexoes_por_ponto[nome] = conexoes
        
        if conexoes_por_ponto:
            ponto_mais_conectado = max(conexoes_por_ponto, key=conexoes_por_ponto.get)
            max_conexoes = conexoes_por_ponto[ponto_mais_conectado]
            print(f"  🌟 Ponto mais conectado: {ponto_mais_conectado} ({max_conexoes} conexões)")
    
    def contar_conexoes(self):
        """Conta o número total de conexões na rede"""
        conexoes = 0
        for i in range(len(self.grafo.matriz)):
            for j in range(i + 1, len(self.grafo.matriz)):
                if self.grafo.matriz[i][j] != float('inf'):
                    conexoes += 1
        return conexoes
