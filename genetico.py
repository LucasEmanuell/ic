import random
import matplotlib.pyplot as plt
def four_peaks_fitness(bitstring, T, R):
    N = len(bitstring)
    max_ones = max_zeros = 0

    # Contagem de 1's consecutivos no início
    for bit in bitstring:
        if bit == 1:
            max_ones += 1
        else:
            break

    # Contagem de 0's consecutivos no final
    for bit in reversed(bitstring):
        if bit == 0:
            max_zeros += 1
        else:
            break

    # Cálculo do bônus
    if max_ones > T and max_zeros > T:
        return max(max_ones, max_zeros) + R
    else:
        return max(max_ones, max_zeros)
def genetic_algorithm(N=30, T=5, R=10, population_size=50, mutation_rate=0.01, crossover_rate=0.8, generations=100):
    # Inicialização da população
    population = [[random.randint(0, 1) for _ in range(N)] for _ in range(population_size)]

    best_fitness_history = []
    average_fitness_history = []

    for generation in range(generations):
        # Avaliação da população
        fitness_values = [four_peaks_fitness(individual, T, R) for individual in population]
        best_fitness = max(fitness_values)
        average_fitness = sum(fitness_values) / population_size

        best_fitness_history.append(best_fitness)
        average_fitness_history.append(average_fitness)

        # Seleção por torneio
        selected = []
        for _ in range(population_size):
            i, j = random.sample(range(population_size), 2)
            if fitness_values[i] > fitness_values[j]:
                selected.append(population[i])
            else:
                selected.append(population[j])

        # Crossover e mutação
        next_generation = []
        for i in range(0, population_size, 2):
            parent1 = selected[i]
            parent2 = selected[i+1] if i+1 < population_size else selected[0]

            # Crossover
            if random.random() < crossover_rate:
                point = random.randint(1, N-1)
                offspring1 = parent1[:point] + parent2[point:]
                offspring2 = parent2[:point] + parent1[point:]
            else:
                offspring1 = parent1[:]
                offspring2 = parent2[:]

            # Mutação
            for offspring in [offspring1, offspring2]:
                for idx in range(N):
                    if random.random() < mutation_rate:
                        offspring[idx] = 1 - offspring[idx]

                next_generation.append(offspring)

        population = next_generation[:population_size]  # Garante que a população mantém o tamanho correto

    # Obtenção do melhor indivíduo final
    fitness_values = [four_peaks_fitness(individual, T, R) for individual in population]
    best_fitness = max(fitness_values)
    best_individual = population[fitness_values.index(best_fitness)]

    # Impressão dos resultados
    print("Melhor Solução Encontrada:")
    print(best_individual)
    print("Fitness da Melhor Solução:", best_fitness)

    # Gráfico de convergência
    plt.plot(best_fitness_history, label='Melhor Fitness')
    plt.plot(average_fitness_history, label='Fitness Médio')
    plt.title('Convergência do Algoritmo Genético')
    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()

    return best_individual, best_fitness, best_fitness_history, average_fitness_history

# Execução do algoritmo
best_solution, best_fitness, best_fitness_history, average_fitness_history = genetic_algorithm()
