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
INDIVIDUOS_CRUZAMENTO = 40

# criar um indivíduo viável (peso <= 15kg)
def criar_individuo_viavel():
    while True:
        individuo = [random.randint(0, 1) for _ in range(len(itens))] # seleciona um valor binário (0 ou 1) para representar a quantidade de cada item na solução
        peso = calcular_peso(individuo) # calcula o peso para garantir que é menor ou igual a 15kg
        if peso <= CAPACIDADE:
            return individuo # só retorna o indivíduo criado se ele for factível

# calcular o peso de um indivíduo
def calcular_peso(individuo):
    return sum(itens[i]['peso'] for i in range(len(individuo)) if individuo[i] == 1)

# calcular o valor de um indivíduo factível
def calcular_valor(individuo):
    peso = calcular_peso(individuo)
    if peso > CAPACIDADE:
        return 0
    return sum(itens[i]['valor'] for i in range(len(individuo)) if individuo[i] == 1)

# seleção por roleta (todos os indivíduos tem a mesma chance de serem selecionados)
def selecao_roleta_proporcional(populacao, valores, k):
    # calcula o valor total da população
    total_valor = sum(valores)
    
    # calcula as probabilidades proporcionalmente aos valores
    probabilidades = [v/total_valor for v in valores]
    
    # seleciona k indivíduos com probabilidade proporcional ao seu valor
    return random.choices(populacao, weights=probabilidades, k=k)

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
def mutacao(individuo, max_tentativas=10):
    tentativas = 0
    while tentativas < max_tentativas:
        # cria uma cópia do indivíduo para modificar
        individuo_mutado = individuo.copy()
        
        # sorteia o gene a ser mutado
        gene = random.randint(0, len(individuo_mutado)-1)
        
        # inverte o valor do gene (0 vira 1, 1 vira 0)
        individuo_mutado[gene] = 1 - individuo_mutado[gene]
        
        # verifica se a mutação resultou em um indivíduo viável
        if calcular_peso(individuo_mutado) <= CAPACIDADE:
            return individuo_mutado

        tentativas += 1
    
    # se não encontrou uma mutação válida após 10 tentativas, retorna o original para não entrar em loop infinito
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
        print(f"Melhor indivíduo: {melhor_individuo}")
        print(f"Valor: R${melhor_valor}")
        print(f"Peso: {calcular_peso(melhor_individuo)} kg")
        print(f"Itens: {[itens[i]['nome'] for i in range(len(melhor_individuo)) if melhor_individuo[i] == 1]}")
        
        # selecionar 40 indivíduos para cruzamento (com probabilidade proporcional ao valor)
        pais = selecao_roleta_proporcional(populacao, valores, INDIVIDUOS_CRUZAMENTO)
        
        # realizar cruzamento para gerar 40 filhos
        filhos = []
        for i in range(0, INDIVIDUOS_CRUZAMENTO, 2):
            pai1, pai2 = pais[i], pais[i+1]
            filho1, filho2 = crossover(pai1, pai2)
            
            if random.random() <= TAXA_MUTACAO:
                filho1 = mutacao(filho1)
            if random.random() <= TAXA_MUTACAO:
                filho2 = mutacao(filho2)
            
            filhos.extend([filho1, filho2])
        
        # 10 indivíduos não selecionados p/ cruzamento são mantidos na próxima geração
        mantidos =  [ind for ind in populacao if ind not in pais]

        # nova população = filhos + mantidos
        nova_populacao = filhos + mantidos
        
        #print(f"Indivíduos selecionados para cruzamento: {len(pais)}")
        #print(f"Filhos gerados: {len(filhos)}")
        #print(f"Indivíduos mantidos: {len(mantidos)}")
        #print(f"Total na nova geração: {len(nova_populacao)}")
        
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