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
def hill_climbing(N=30, T=5, R=10, max_iterations=1000):
    # Inicialização aleatória
    current_solution = [random.randint(0, 1) for _ in range(N)]
    current_fitness = four_peaks_fitness(current_solution, T, R)
    fitness_history = [current_fitness]

    for iteration in range(max_iterations):
        neighbors = []
        # Geração de vizinhos alterando um bit de cada vez
        for i in range(N):
            neighbor = current_solution.copy()
            neighbor[i] = 1 - neighbor[i]  # Flip do bit
            neighbors.append(neighbor)

        # Avaliação dos vizinhos
        neighbor_fitness = [four_peaks_fitness(neighbor, T, R) for neighbor in neighbors]
        best_neighbor_index = neighbor_fitness.index(max(neighbor_fitness))
        best_neighbor = neighbors[best_neighbor_index]
        best_neighbor_fitness = neighbor_fitness[best_neighbor_index]

        # Verificação de melhoria
        if best_neighbor_fitness > current_fitness:
            current_solution = best_neighbor
            current_fitness = best_neighbor_fitness
            fitness_history.append(current_fitness)
        else:
            # Se nenhum vizinho é melhor, termina a busca
            break

    return current_solution, current_fitness, fitness_history

# Execução do algoritmo
best_solution, best_fitness, fitness_history = hill_climbing()

# Impressão dos resultados
print("Melhor Solução Encontrada:")
print(best_solution)
print("Fitness da Melhor Solução:", best_fitness)

# Gráfico de convergência
plt.plot(fitness_history)
plt.title('Convergência da Subida de Encosta')
plt.xlabel('Iteração')
plt.ylabel('Fitness')
plt.show()
