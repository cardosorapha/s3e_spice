import numpy as np
from matplotlib import pyplot as plt

# -------------------------------------------- #
# Faz a simulacao estatica de um circuito      #
# puramente resistivo. Caso uma simulacao      #
# transiente seja desejada, basta executar     #
# essa funcao num loop de amostras para        #
# a entrada.                                   #
#                                              #
# Input:                                       #
#   - entrada: valor de tensao da fonte Vs     #
#                                              #
# Output:                                      #
#   - tensoes_correntes: vetor com todas       #
#      as tensoes e correntes do circuito      #
# -------------------------------------------- #
def exemplo_1(entrada, R1, R2, R3, R4):
    # A x k = B
    # Realiza a inversao de A para encontrar k
    B = np.array([entrada,0,0,0,0,0,0,0,0,0])
    A = np.array([[1,0,0,0,0,0,0,0,0,0],\
                 [0,1,0,0,0,-R1,0,0,0,0],\
                 [0,0,1,0,0,0,-R2,0,0,0],\
                 [0,0,0,1,0,0,0,-R3,0,0],\
                 [0,0,0,0,1,0,0,0,-R4,0],\
                 [-1,1,0,1,0,0,0,0,0,0],\
                 [0,0,1,-1,1,0,0,0,0,0],\
                 [0,0,0,0,0,-1,0,0,0,-1],\
                 [0,0,0,0,0,1,-1,-1,0,0],\
                 [0,0,0,0,0,0,1,0,-1,0]])
    tensoes_correntes = np.matmul(np.linalg.inv(A),B)

    return tensoes_correntes

def simulacao_1():
### 1 ###
# Simulacao DC para todos resistores de 1K
    resultado_1 = exemplo_1(5,R1=1e3,R2=1e3,R3=2e3,R4=1e3)
    print('##################################')
    print('Simulacao 1')
    print(f'Tensao sobre R4: {resultado_1[4]}V')
    print('##################################')

def simulacao_2():
### 2 ###
# Varredura para diferentes valores de R1
    R1_lista = range(0,1000,100) 
    V4_lista = []
    for R1 in R1_lista:
       resultado_2 = exemplo_1(5,R1=R1,R2=1e3,R3=1e3,R4=1e3) 
       V4_lista.append(resultado_2[4])

    plt.scatter(R1_lista, V4_lista)
    plt.title('Simulacao 2')
    plt.ylabel('Tensao V4')
    plt.xlabel('Valor de R1')
    plt.show()

def simulacao_3():
### 3 ###
# Simulacao transiente para uma senoide de 1kHz em V4
# Parametros de simulacao
    inicio = 0
    fim = 2e-3 # 2ms
    passo = 10e-6 # 10us

# Parametro da entrada
    freq_seno = 1e3 # 1kHz

# Criacao dos vetores
    vetor_tempo = np.arange(inicio, fim, passo)
    vetor_entrada = np.sin(2*np.pi*freq_seno*vetor_tempo)
    vetor_saida = np.zeros_like(vetor_entrada)

    for i in range(len(vetor_tempo)):
        resultado_3 = exemplo_1(vetor_entrada[i],R1=1e3,R2=1e3,R3=1e3,R4=1e3)
        vetor_saida[i] = resultado_3[0] # interessado em V4
    plt.plot(1e3*vetor_tempo,vetor_entrada)
    plt.plot(1e3*vetor_tempo,vetor_saida)
    plt.title('Simulacao 3')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Tensao em V4')
    plt.show()


simulacao_3()
