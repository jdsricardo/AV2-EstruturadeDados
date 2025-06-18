# Sistema de Emergência Médica - AV2 Estrutura de Dados

## 📋 Descrição do Projeto

Este projeto implementa um **sistema de emergência médica** utilizando **grafos** e **matriz de adjacência** para encontrar as rotas mais rápidas entre pontos de atendimento médico na cidade.

## 🎯 Objetivo

Resolver um problema real: otimizar o tempo de deslocamento de ambulâncias e transferências entre hospitais, UPAs e prontos socorros, garantindo atendimento mais eficiente em emergências.

## 🏗️ Estrutura do Projeto

```
AV2-EstruturadeDados/
├── app.py                 # Arquivo principal
├── grafo_emergencia.py    # Classe do grafo com matriz de adjacência
├── visualizador.py        # Visualização gráfica do grafo
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

## 🧩 Classes Principais

### 1. **GrafoEmergencia**
- **Responsabilidade**: Gerenciar a rede de pontos médicos
- **Estrutura de dados**: Matriz de adjacência
- **Funcionalidades**:
  - Adicionar pontos médicos (hospitais, UPAs, prontos socorros)
  - Definir tempos de deslocamento entre pontos
  - Encontrar rota mais rápida (Algoritmo de Dijkstra)
  - Exibir matriz de adjacência

### 2. **VisualizadorGrafo**
- **Responsabilidade**: Criar visualizações do grafo
- **Bibliotecas**: matplotlib, networkx
- **Funcionalidades**:
  - Plotar rede completa de pontos médicos
  - Destacar rotas específicas
  - Salvar gráficos em PNG

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o Sistema
```bash
python app.py
```

## 📊 Exemplo de Funcionamento

O sistema cria uma rede com 6 pontos médicos:
- **Hospital Central** 🏥
- **UPA Norte** 🚑  
- **Hospital São Lucas** 🏥
- **UPA Sul** 🚑
- **Pronto Socorro** ⛑️
- **Hospital Infantil** 🏥

### Matriz de Adjacência (Tempos em minutos):
```
                Hospital Central  UPA Norte  Hospital São Lucas  ...
Hospital Central        0           12            18           ...
UPA Norte              12            0            15           ...
Hospital São Lucas     18           15             0           ...
...
```

### Exemplo de Rota:
```
🚨 EMERGÊNCIA: UPA Norte → Hospital Infantil
Rota mais rápida: UPA Norte → Hospital Infantil
Tempo total: 10 minutos
```

## 🎨 Visualização

O sistema gera um grafo visual com:
- **Nós coloridos** por tipo de estabelecimento
- **Arestas** com tempos de deslocamento
- **Destaque** para rotas específicas

## 🔧 Conceitos de Estrutura de Dados Utilizados

1. **Grafo Não-Direcionado**: Conexões bidirecionais entre pontos
2. **Matriz de Adjacência**: Armazenamento eficiente dos tempos
3. **Algoritmo de Dijkstra**: Busca pela rota mais rápida
4. **Dicionários**: Mapeamento nome ↔ índice dos pontos

## 📈 Possíveis Expansões

- Considerar trânsito em horários diferentes
- Adicionar tipos de ambulância (UTI móvel, resgate)
- Implementar sistema de prioridades
- Integração com GPS real
- Interface gráfica interativa

## 👨‍💻 Autor

**Ricardo José da Silva**  
AV2 - Estrutura de Dados  
Data: 17 de junho de 2025
