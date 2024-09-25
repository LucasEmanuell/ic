import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definindo as variáveis fuzzy
temperatura = ctrl.Antecedent(np.arange(800, 1201, 1), 'temperatura')
pressao = ctrl.Antecedent(np.arange(4, 13, 0.1), 'pressao')
vazao = ctrl.Consequent(np.arange(0, 3.1, 0.1), 'vazao')

# Definindo as funções de pertinência para temperatura
temperatura['baixa'] = fuzz.trapmf(temperatura.universe, [800, 800, 850, 900])
temperatura['media'] = fuzz.trimf(temperatura.universe, [850, 1000, 1150])
temperatura['alta'] = fuzz.trapmf(temperatura.universe, [1100, 1150, 1200, 1200])

# Definindo as funções de pertinência para pressão
pressao['baixa'] = fuzz.gaussmf(pressao.universe, 4, 2)
pressao['media'] = fuzz.gaussmf(pressao.universe, 8, 1.3)
pressao['alta'] = fuzz.gaussmf(pressao.universe, 12, 2)

# Definindo as funções de pertinência para vazão
vazao['baixa'] = fuzz.trapmf(vazao.universe, [0, 0, 0.5, 1])
vazao['media-baixa'] = fuzz.trimf(vazao.universe, [0.5, 1, 1.5])
vazao['media'] = fuzz.trimf(vazao.universe, [1, 1.5, 2])
vazao['media-alta'] = fuzz.trimf(vazao.universe, [1.5, 2, 2.5])
vazao['alta'] = fuzz.trapmf(vazao.universe, [2, 2.5, 3, 3])

# Definindo as regras fuzzy
rule1 = ctrl.Rule(temperatura['baixa'] & pressao['baixa'], vazao['baixa'])
rule2 = ctrl.Rule(temperatura['baixa'] & pressao['media'], vazao['media-baixa'])
rule3 = ctrl.Rule(temperatura['baixa'] & pressao['alta'], vazao['media'])
rule4 = ctrl.Rule(temperatura['media'] & pressao['baixa'], vazao['media-baixa'])
rule5 = ctrl.Rule(temperatura['media'] & pressao['media'], vazao['media'])
rule6 = ctrl.Rule(temperatura['media'] & pressao['alta'], vazao['media-alta'])
rule7 = ctrl.Rule(temperatura['alta'] & pressao['baixa'], vazao['media'])
rule8 = ctrl.Rule(temperatura['alta'] & pressao['media'], vazao['media-alta'])
rule9 = ctrl.Rule(temperatura['alta'] & pressao['alta'], vazao['alta'])

# Criando o sistema de controle fuzzy para Mamdani
vazao_ctrl_mamdani = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
vazao_simulation_mamdani = ctrl.ControlSystemSimulation(vazao_ctrl_mamdani)

# Criando o sistema de controle fuzzy para Larsen (multiplicativo)
vazao_ctrl_larsen = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
vazao_simulation_larsen = ctrl.ControlSystemSimulation(vazao_ctrl_larsen)

# Função para defuzzificação pela Média dos Máximos (MoM)
def mean_of_maximum(x, mfx):
    max_mf = np.max(mfx)
    mean_max = np.mean(x[mfx == max_mf])
    return mean_max

# Lista de testes de temperatura e pressão
temperaturas = [850, 900, 1000, 1100, 1150, 880, 950, 1049, 1089, 1170]
pressoes = [8, 4.5, 9, 10, 5, 7, 7, 8, 9, 7]
vazao_desejada = [1.01, 0.42, 1.63, 1.7, 2.43, 1.07, 1.41, 1.26, 1.97, 2.15]

# Resultados para armazenar erros
resultados = []

# Calculando a saída de vazão para cada par de temperatura e pressão
for i, (temp, press, vazao_ref) in enumerate(zip(temperaturas, pressoes, vazao_desejada)):
    # Simulação Mamdani
    vazao_simulation_mamdani.input['temperatura'] = temp
    vazao_simulation_mamdani.input['pressao'] = press
    vazao_simulation_mamdani.compute()
    
    # Defuzzificação Mamdani (Centroid)
    vazao_mamdani_centroid = vazao_simulation_mamdani.output['vazao']
    
    # Defuzzificação Mamdani (MoM)
    vazao_mamdani_mom = mean_of_maximum(vazao.universe, fuzz.interp_membership(vazao.universe, vazao['media'].mf, vazao_simulation_mamdani.output['vazao']))

    # Simulação Larsen
    vazao_simulation_larsen.input['temperatura'] = temp
    vazao_simulation_larsen.input['pressao'] = press
    vazao_simulation_larsen.compute()

    # Defuzzificação Larsen (Centroid)
    vazao_larsen_centroid = vazao_simulation_larsen.output['vazao']

    # Defuzzificação Larsen (MoM)
    vazao_larsen_mom = mean_of_maximum(vazao.universe, fuzz.interp_membership(vazao.universe, vazao['media'].mf, vazao_simulation_larsen.output['vazao']))
    
    # Calculando o erro relativo para cada método
    erro_mamdani_centroid = abs(vazao_ref - vazao_mamdani_centroid) / vazao_ref * 100
    erro_mamdani_mom = abs(vazao_ref - vazao_mamdani_mom) / vazao_ref * 100
    erro_larsen_centroid = abs(vazao_ref - vazao_larsen_centroid) / vazao_ref * 100
    erro_larsen_mom = abs(vazao_ref - vazao_larsen_mom) / vazao_ref * 100
    
    resultados.append([i+1, temp, press, vazao_ref, vazao_mamdani_centroid, erro_mamdani_centroid, 
                       vazao_mamdani_mom, erro_mamdani_mom, vazao_larsen_centroid, erro_larsen_centroid,
                       vazao_larsen_mom, erro_larsen_mom])

# Calculando o erro relativo médio
def calcular_erm(erros):
    return np.mean(erros)

# Exibindo os resultados
print(f'{"Teste":<6}{"Temp":<6}{"Press":<6}{"Ref":<6}{"Mamd-Cen":<9}{"Err-MC":<8}{"Mamd-MoM":<9}{"Err-MM":<8}{"Lars-Cen":<9}{"Err-LC":<8}{"Lars-MoM":<9}{"Err-LM":<8}')
for r in resultados:
    print(f'{r[0]:<6}{r[1]:<6}{r[2]:<6}{r[3]:<6.2f}{r[4]:<9.2f}{r[5]:<8.2f}{r[6]:<9.2f}{r[7]:<8.2f}{r[8]:<9.2f}{r[9]:<8.2f}{r[10]:<9.2f}{r[11]:<8.2f}')
    
# Calculando o erro relativo médio para cada método
erm_mamdani_centroid = calcular_erm([r[5] for r in resultados])
erm_mamdani_mom = calcular_erm([r[7] for r in resultados])
erm_larsen_centroid = calcular_erm([r[9] for r in resultados])
erm_larsen_mom = calcular_erm([r[11] for r in resultados])

print(f'\nErro Relativo Médio (ERM):')
print(f'Mamdani - Centroid: {erm_mamdani_centroid:.2f}%')
print(f'Mamdani - MoM: {erm_mamdani_mom:.2f}%')
print(f'Larsen - Centroid: {erm_larsen_centroid:.2f}%')
print(f'Larsen - MoM: {erm_larsen_mom:.2f}%')

# Determinando o melhor sistema fuzzy com base no menor ERM
min_erm = min(erm_mamdani_centroid, erm_mamdani_mom, erm_larsen_centroid, erm_larsen_mom)
if min_erm == erm_mamdani_centroid:
    melhor_metodo = "Mamdani - Centroid"
elif min_erm == erm_mamdani_mom:
    melhor_metodo = "Mamdani - MoM"
elif min_erm == erm_larsen_centroid:
    melhor_metodo = "Larsen - Centroid"
else:
    melhor_metodo = "Larsen - MoM"

print(f'\nMelhor sistema fuzzy para implementar o controlador é: {melhor_metodo} com ERM de {min_erm:.2f}%')