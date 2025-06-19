# Sistema de Rotas entre Hospitais 🏥

## Descrição do Projeto

Sistema simples que implementa **grafos** com **matriz de adjacência** para calcular tempos de trajeto entre hospitais considerando condições de trânsito em tempo real. Perfeito para demonstrar conceitos de estrutura de dados com problema real.

## Problema Real

- **Situação**: Ambulâncias precisam saber o tempo de deslocamento entre hospitais
- **Solução**: Matriz de adjacência com multiplicadores de trânsito aleatórios
- **Aplicação**: Logística médica, transferências de emergência

## Funcionalidades

1. **Consulta de Tempo**: Calcula tempo entre dois hospitais específicos
2. **Mapa Visual**: Mostra cidade com ruas, quarteirões e condições de trânsito
3. **Trânsito Dinâmico**: Condições aleatórias a cada visualização

## Arquivos

- `app.py` - Programa principal (76 linhas)
- `mapa_visual.py` - Visualização do mapa (180 linhas)
- `requirements.txt` - Dependências

## Como Usar

1. **Instalar dependências:**
```bash
pip install numpy matplotlib
```

2. **Executar:**
```bash
python app.py
```

3. **Menu:**
   - **Opção 1**: Consultar tempo entre hospitais
   - **Opção 2**: Ver mapa visual da cidade
   - **Opção 3**: Sair

## Estrutura dos Dados

### Hospitais:
- Hospital Central
- UPA Norte  
- Hospital São Lucas
- UPA Sul
- Hospital Infantil

### Matriz de Adjacência (5x5):
```
         HC  UN  HSL  US  HI
HC    [  0, 12, 18, 15, 22 ]
UN    [ 12,  0, 25, 30, 20 ]
HSL   [ 18, 25,  0, 14,  8 ]
US    [ 15, 30, 14,  0, 16 ]
HI    [ 22, 20,  8, 16,  0 ]
```

### Multiplicadores de Trânsito:
- **0.8 - 1.2**: Trânsito livre (verde)
- **1.2 - 1.8**: Trânsito moderado (laranja)  
- **1.8 - 2.2**: Congestionamento (vermelho)

## Exemplo de Uso

```
🏥 SISTEMA DE ROTAS ENTRE HOSPITAIS
========================================

1. Consultar tempo entre hospitais
2. Visualizar mapa da cidade
3. Sair

Opção: 1

Hospitais disponíveis:
0. Hospital Central
1. UPA Norte
2. Hospital São Lucas
3. UPA Sul
4. Hospital Infantil

Origem: 0
Destino: 4

🚑 Tempo estimado: 28.6 minutos
   Hospital Central → Hospital Infantil
```

## Conceitos Demonstrados

- **Grafos**: Representação da rede de hospitais
- **Matriz de Adjacência**: Armazenamento eficiente dos pesos
- **Simulação Probabilística**: Condições de trânsito variáveis

## Mapa Visual

O sistema gera um mapa realista com:
- 🏘️ **Quarteirões**: Residenciais, comerciais e parque
- �️ **Ruas**: Avenidas principais e ruas secundárias  
- 🏥 **Hospitais**: Com ícones diferenciados
- 🚦 **Trânsito**: Cores indicando condições atuais

Desenvolvido para AV2 - Estrutura de Dados
