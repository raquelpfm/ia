# ALTERAÇÃO NA CRIAÇÃO DE NOVA GERAÇÃO

# Número de cruzamentos é dado por 0,8 * tamanho da população dividido por 2
# Um mesmo pai pode ser selecionado para cruzar mais de uma vez em uma geração
# Portanto, podem sobrar mais de 10 pais não selecionados para cruzamento em uma geração
# Todos eles são mantidos para a geração seguinte, juntamente aos novos filhos gerados
# A nova população cresce rapidamente

import random
import matplotlib.pyplot as plt

itens = [
    {'nome': 'A', 'peso': 2, 'valor': 40},
    {'nome': 'B', 'peso': 3, 'valor': 50},
    {'nome': 'C', 'peso': 4, 'valor': 65},
    {'nome': 'D', 'peso': 5, 'valor': 80},
    {'nome': 'E', 'peso': 7, 'valor': 110},
    {'nome': 'F', 'peso': 1, 'valor': 15},
    {'nome': 'G', 'peso': 6, 'valor': 90},
    {'nome': 'H', 'peso': 4.5, 'valor': 70},
    {'nome': 'I', 'peso': 3.5, 'valor': 60},
    {'nome': 'J', 'peso': 2.5, 'valor': 55}
]

CAPACIDADE = 15 
TAMANHO_POPULACAO = 50
NUM_GERACOES = 200
TAXA_CRUZAMENTO = 0.8
TAXA_MUTACAO = 0.05
NUM_PARES_CRUZAMENTO = int((TAMANHO_POPULACAO * TAXA_CRUZAMENTO) / 2)  # 20 pares

# criar um indivíduo viável (peso <= 15kg)
def criar_individuo_viavel():
    while True:
        individuo = [random.randint(0, 1) for _ in range(len(itens))] # seleciona um valor binário (0 ou 1) para representar a quantidade de dado item na solução
        peso = calcular_peso(individuo) # calcula o peso para garantir que é menor ou igual a 15kg
        if peso <= CAPACIDADE:
            return individuo # só retorna o indivíduo criado se ele for factível

# calcular o peso de um indivíduo
def calcular_peso(individuo):
    return sum(itens[i]['peso'] for i in range(len(individuo)) if individuo[i] == 1)

# calcular o valor de um indivíduo
def calcular_valor(individuo):
    peso = calcular_peso(individuo)
    if peso > CAPACIDADE:
        return 0
    return sum(itens[i]['valor'] for i in range(len(individuo)) if individuo[i] == 1)

# seleção por roleta
def selecao_roleta(populacao, valores):
    total_valor = sum(valores)
    probabilidades = [v/total_valor for v in valores]
    return random.choices(populacao, weights=probabilidades, k=2)

# crossover de 1 ou 2 pontos
def crossover(pai1, pai2):
    # sorteia duas posições X e Y (0 a 9, podendo ser iguais)
    X = random.randint(0, 9)
    Y = random.randint(0, 9)
    
    # cria os filhos como cópias dos pais
    filho1 = pai1.copy()
    filho2 = pai2.copy()
    
    # troca o gene na posição X
    filho1[X], filho2[X] = filho2[X], filho1[X]
    
    # se X for diferente de Y, troca o gene na posição Y
    if X != Y:
        filho1[Y], filho2[Y] = filho2[Y], filho1[Y]
    
    # garante que os filhos são viáveis e refaz o cruzamento caso algum ultrapasse o peso máximo
    while calcular_peso(filho1) > CAPACIDADE or calcular_peso(filho2) > CAPACIDADE:
        X = random.randint(0, 9)
        Y = random.randint(0, 9)
        
        filho1 = pai1.copy()
        filho2 = pai2.copy()
        
        filho1[X], filho2[X] = filho2[X], filho1[X]
        
        if X != Y:
            filho1[Y], filho2[Y] = filho2[Y], filho1[Y]
    
    return filho1, filho2

# mutação
def mutacao(individuo):
    if random.random() <= TAXA_MUTACAO:
        # escolhe qual filho sofrerá mutação (0 ou 1)
        filho_mutado = individuo.copy()
        
        # sorteia o gene a ser mutado
        gene = random.randint(0, len(filho_mutado)-1)
        
        # inverte o valor do gene
        filho_mutado[gene] = 1 - filho_mutado[gene]
        
        # verifica se a mutação resultou em um indivíduo viável
        if calcular_peso(filho_mutado) <= CAPACIDADE:
            return filho_mutado
    
    return individuo

# algoritmo genético
def algoritmo_genetico():
    # criação da população inicial (50 indivíduos factíveis)
    populacao = [criar_individuo_viavel() for _ in range(TAMANHO_POPULACAO)]
    melhor_historico = []
    melhor_global = None
    melhor_valor_global = -1
    
    for geracao in range(NUM_GERACOES):
        # calcula o valor de cada indivíduo
        valores = [calcular_valor(ind) for ind in populacao]
        
        # identifica o melhor da geração atual
        melhor_valor = max(valores)
        melhor_idx = valores.index(melhor_valor)
        melhor_individuo = populacao[melhor_idx]
        
        # atualiza o melhor global
        if melhor_valor > melhor_valor_global:
            melhor_valor_global = melhor_valor
            melhor_global = melhor_individuo
        
        # armazena o histórico do melhor valor
        melhor_historico.append(melhor_valor)
        
        # imprime informações da geração atual
        print(f"\nGeração {geracao + 1}:")
        print(f"Tamanho da população: {len(populacao)}")
        #print(f"Melhor indivíduo: {melhor_individuo}")
        #print(f"Valor: R${melhor_valor}")
        #print(f"Peso: {calcular_peso(melhor_individuo)} kg")
        #print(f"Itens: {[itens[i]['nome'] for i in range(len(melhor_individuo)) if melhor_individuo[i] == 1]}")
        
        # cálculo dinâmico do número de pares para cruzamento
        num_pares = int(len(populacao) * TAXA_CRUZAMENTO) // 2
        # seleção dos pais para cruzamento (20 pares)
        nova_populacao = []
        pais_selecionados = []
        
        for _ in range(num_pares):
            # seleciona dois pais por roleta
            pai1, pai2 = selecao_roleta(populacao, valores)
            pais_selecionados.extend([pai1, pai2])
            
            # cruzamento (gera dois filhos)
            filho1, filho2 = crossover(pai1, pai2)
            
            # mutação (aplicada com 5% de probabilidade)
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)
            
            nova_populacao.extend([filho1, filho2])
        
        # identifica os não selecionados
        nao_selecionados = [ind for ind in populacao if ind not in pais_selecionados]

        # adiciona os não selecionados à nova população
        nova_populacao.extend(nao_selecionados)

        # verificação de consistência
        print(f"Indivíduos gerados por cruzamento: {num_pares * 2}")
        print(f"Indivíduos não selecionados mantidos: {len(nao_selecionados)}")
        #print(f"Total na nova geração: {len(nova_populacao)}")
        
        # garante que a população mantém o tamanho correto
        populacao = nova_populacao
    
    # resultado final
    print("\n=== MELHOR SOLUÇÃO ENCONTRADA ===")
    print(f"Indivíduo: {melhor_global}")
    print(f"Valor: R${melhor_valor_global}")
    print(f"Peso: {calcular_peso(melhor_global)} kg")
    print(f"Itens selecionados: {[itens[i]['nome'] for i in range(len(melhor_global)) if melhor_global[i] == 1]}")
    
    # gráfico de convergência
    plt.figure(figsize=(10, 6))
    plt.plot(melhor_historico, 'b-')
    plt.title("Convergência do Algoritmo Genético")
    plt.xlabel("Geração")
    plt.ylabel("Melhor Valor (R$)")
    plt.grid(True)
    plt.show()

# executa o algoritmo
algoritmo_genetico()