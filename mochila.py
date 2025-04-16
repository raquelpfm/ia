import random

# parâmetros dos itens: peso, valor e quantidade máxima
items = [
    {"weight": 3, "value": 40, "max_quantity": 3},  # item 1
    {"weight": 5, "value": 100, "max_quantity": 2}, # item 2
    {"weight": 2, "value": 50, "max_quantity": 5}   # item 3
]

# capacidade máxima de peso da mochila
capacity = 20

# função objetivo (valor total) se o peso for permitido, senão 0
def fitness(individual):
    # calcula o peso total do indivíduo
    total_weight = sum(gene * item["weight"] for gene, item in zip(individual, items))

    # calcula o valor total do indivíduo
    total_value = sum(gene * item["value"] for gene, item in zip(individual, items))

    # se o peso for maior que a capacidade retorna 0 (indivíduo inválido)
    return total_value if total_weight <= capacity else 0

# criação de indivíduo
def create_individual():
    while True:
        # gera um cromossomo aleatório [X1, X2, X3] respeitando o limite de quantidade de cada item
        individual = [random.randint(0, item["max_quantity"]) for item in items] 

        # se ultrapassar o peso máximo imprime que é inválido e tenta novamente, retorna apenas indivíduos válidos
        if fitness(individual) > 0:
            return individual
        else:
            print(f"Indivíduo inválido (peso excedido): {individual}. Gerando novo...")

# Criação da população inicial
def create_population():
    return [create_individual() for _ in range(4)]

# Função de crossover conforme seu exemplo
def crossover(population):
    population_sorted = sorted(population, key=fitness, reverse=True)
    best_half = population_sorted[:2]
    worst_half = population_sorted[-2:]

    print("\nDividindo população:")
    print(f"Melhores: {best_half}")
    print(f"Piores: {worst_half}")

    new_population = []

    for i in range(2):
        parent1 = best_half[i]
        parent2 = worst_half[i]

        child1 = parent1.copy()
        child2 = parent2.copy()

        num_genes = random.randint(1, 2)
        genes_to_swap = random.sample(range(len(items)), num_genes)

        print(f"\nCruzamento {i+1}:")
        print(f"Pais -> {parent1} & {parent2}")
        print(f"Genes sorteados para troca: {genes_to_swap}")

        for gene_index in genes_to_swap:
            child1[gene_index], child2[gene_index] = parent2[gene_index], parent1[gene_index]

        print(f"Filhos gerados: {child1} e {child2}")
        new_population.extend([child1, child2])

    return new_population

# Mutação com 10% de chance
def mutate(individual):
    if random.random() < 0.1:
        gene_index = random.randint(0, len(items) - 1)
        old_value = individual[gene_index]
        individual[gene_index] = random.randint(0, items[gene_index]["max_quantity"])
        print(f"Mutação! Gene {gene_index} alterado de {old_value} para {individual[gene_index]}")
    return individual

# Algoritmo principal com Best registrado
def genetic_algorithm():
    population = create_population()

    print("\nPopulação Inicial:")
    labels = ['A', 'B', 'C', 'D']
    for label, individual in zip(labels, population):
        print(f"{label}: {individual} | Valor: {fitness(individual)}")

    best_solution = max(population, key=fitness)
    best_value = fitness(best_solution)
    print(f"\nMelhor valor inicial (Best): {best_value} - Solução: {best_solution}")

    no_improvement = 0
    generation = 0

    while no_improvement < 2:
        generation += 1
        print(f"\n=== Geração {generation} ===")

        # Cruzamento
        population = crossover(population)

        # Mutação aplicada e verificação
        for i in range(len(population)):
            population[i] = mutate(population[i])

            # Se infactível, substituir
            if fitness(population[i]) == 0:
                print(f"Indivíduo {i+1} infactível após mutação: {population[i]}. Substituindo...")
                population[i] = create_individual()
                print(f"Novo indivíduo {i+1}: {population[i]} | Valor: {fitness(population[i])}")

        # Exibir nova população
        print("\nNova População:")
        for idx, individual in enumerate(population):
            print(f"Indivíduo {idx+1}: {individual} | Valor: {fitness(individual)}")

        # Avalia a geração
        current_best = max(population, key=fitness)
        current_value = fitness(current_best)

        if current_value > best_value:
            best_solution = current_best
            best_value = current_value
            no_improvement = 0
            print(f"\nNovo Best encontrado! Valor: {best_value} | Solução: {best_solution}")
        else:
            no_improvement += 1
            print(f"\nNenhuma melhora. Best continua: {best_value} | Solução: {best_solution}")

    print("\n==== Melhor Solução Final ====")
    print(f"Solução: {best_solution}")
    print(f"Valor Total: {best_value}")

# Executar o algoritmo
genetic_algorithm()
