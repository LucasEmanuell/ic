import numpy as np
import matplotlib.pyplot as plt

# Definindo as funções de pertinência
def mu_A(x):
    return x / (x + 1)

def mu_B(x):
    return 1 / (x**2 + 10)

def mu_C(x):
    return 1 / (10**x)

# Definindo os complementos das funções de pertinência
def mu_complement_A(x):
    return 1 - mu_A(x)

def mu_complement_B(x):
    return 1 - mu_B(x)

def mu_complement_C(x):
    return 1 - mu_C(x)

# Definindo as operações entre os conjuntos fuzzy
def fuzzy_union(mu1, mu2, x):
    return np.maximum(mu1(x), mu2(x))

def fuzzy_intersection(mu1, mu2, x):
    return np.minimum(mu1(x), mu2(x))

# Gerando os gráficos
x = np.linspace(0, 10, 400)

# Calculando as funções de pertinência resultantes
union_AB = fuzzy_union(mu_A, mu_B, x)
intersection_BC = fuzzy_intersection(mu_B, mu_C, x)
union_ABC = np.maximum.reduce([mu_A(x), mu_B(x), mu_C(x)])
intersection_ABC = np.minimum.reduce([mu_A(x), mu_B(x), mu_C(x)])
intersection_A_complementC = fuzzy_intersection(mu_A, mu_complement_C, x)
intersection_complementB_C = fuzzy_intersection(mu_complement_B, mu_C, x)
intersection_A_complementB = fuzzy_intersection(mu_A, mu_complement_B, x)
union_complementA_complementB = fuzzy_union(mu_complement_A, mu_complement_B, x)

# Plotando os gráficos
plt.figure(figsize=(15, 10))

# Gráfico (a)
plt.subplot(2, 2, 1)
plt.plot(x, union_AB, label=r'$\mu_{A \cup B}(x)$', color='blue')
plt.plot(x, intersection_BC, label=r'$\mu_{B \cap C}(x)$', color='green')
plt.title('(a) União de A e B, Interseção de B e C')
plt.xlabel('x')
plt.ylabel('Grau de Pertinência')
plt.legend()

# Gráfico (b)
plt.subplot(2, 2, 2)
plt.plot(x, union_ABC, label=r'$\mu_{A \cup B \cup C}(x)$', color='blue')
plt.plot(x, intersection_ABC, label=r'$\mu_{A \cap B \cap C}(x)$', color='green')
plt.title('(b) União de A, B e C, Interseção de A, B e C')
plt.xlabel('x')
plt.ylabel('Grau de Pertinência')
plt.legend()

# Gráfico (c)
plt.subplot(2, 2, 3)
plt.plot(x, intersection_A_complementC, label=r'$\mu_{A \cap \overline{C}}(x)$', color='blue')
plt.plot(x, intersection_complementB_C, label=r'$\mu_{\overline{B} \cap C}(x)$', color='green')
plt.title('(c) Interseção de A e complemento de C, complemento de B e C')
plt.xlabel('x')
plt.ylabel('Grau de Pertinência')
plt.legend()

# Gráfico (d)
plt.subplot(2, 2, 4)
plt.plot(x, intersection_A_complementB, label=r'$\mu_{A \cap \overline{B}}(x)$', color='blue')
plt.plot(x, union_complementA_complementB, label=r'$\mu_{\overline{A} \cup \overline{B}}(x)$', color='green')
plt.title('(d) Interseção de A e complemento de B, união de complementos de A e B')
plt.xlabel('x')
plt.ylabel('Grau de Pertinência')
plt.legend()

plt.tight_layout()
plt.show()
