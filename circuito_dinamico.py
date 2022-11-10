import numpy as np
from matplotlib import pyplot as plt

# -------------------------------------------- #
# Faz a simulacao estatica de um circuito      #
# RC. Caso uma simulacao transiente seja       #
# desejada, use exemplo_2.                     #
#                                              #
# Esta funcao retorna resultados em            #
#           **steady state**                   # 
#                                              #
# Input:                                       #
#   - entrada: valor de tensao da fonte Vs     #
#   - frequencia: valor da frequencia          #
#                 de operacao (Hz)             #
#                                              #
# Output:                                      #
#   - tensoes_correntes: vetor com todas       #
#      as tensoes e correntes do circuito      #
# -------------------------------------------- #
def exemplo_1(entrada, frequencia, R1, C2):
    w = 2*np.pi*frequencia
    # A x k = B
    # Realiza a inversao de A para encontrar k
    B = np.array([entrada,0,0,0,0,0])
    A = np.array([[1,0,0,0,0,0],\
                 [0,1,0,0,-R1,0],\
                 [0,0,1j*w*C2,0,0,-1],\
                 [-1,1,1,0,0,0],\
                 [0,0,0,-1,-1,0],\
                 [0,0,0,0,1,-1]])
    tensoes_correntes = np.matmul(np.linalg.inv(A),B)

    return tensoes_correntes

# -------------------------------------------- #
# Faz a simulacao transiente de um circuito    #
# RC do circuito.                              #
#                                              #
# Input:                                       #
#   - entrada: valor de tensao do degrau em Vs #
#   - Vcap: tensao no capacitor                #
#   - ts: tempo de amostragem                  #
#   - tmax: tempo total de simulacao           #
#                                              #
# Output:                                      #
#   - tensoes_correntes: valores de um passo   #
#                        da simulacao
# -------------------------------------------- #
def exemplo_2(entrada, Vcap, ts, tmax, R1, C2):
    
    # A x k = B
    # Realiza a inversao de A para encontrar k
    B = np.array([entrada,0,0,-Vcap,0,0])
    A = np.array([[1,0,0,0,0,0],\
                 [0,1,0,0,-R1,0],\
                 [0,0,-C2,0,0,1],\
                 [-1,1,0,0,0,0],\
                 [0,0,0,-1,-1,0],\
                 [0,0,0,0,1,-1]])
    tensoes_correntes = np.matmul(np.linalg.inv(A),B)
    return tensoes_correntes

def simulacao_1():
### 1 ###
# Diagrama de bode do circuito
    f_lista = np.logspace(1,4,400)
    V2_lista = np.zeros_like(f_lista)

    magnitude_entrada = 5
    for i in range(len(f_lista)):
        resultado_1 = exemplo_1(magnitude_entrada,frequencia=f_lista[i],R1=1591.5,C2=1e-6)
        amplitude = np.abs(resultado_1[2]) # Interessado em V2
        V2_lista[i] = 20*np.log10(amplitude/magnitude_entrada)

    plt.semilogx(f_lista,V2_lista)
    plt.title('Simulacao 1')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Amplitude V2')
    plt.show()

def simulacao_2():
### 2 ###
# Simulacao transiente do circuito RC
    tmax = 5e-9 # 5ms
    ts = 1e-12 # 1us

    degrau_amplitude = 5

    vetor_tempo = np.arange(0,tmax,ts)
    vetor_saida = np.zeros_like(vetor_tempo)

    V2 = 0 # Inicializando a tensao no capacitor
    for i in range(len(vetor_tempo)):
        vetor_saida[i] = V2 # Gravando o valor de V2 no vetor

        # Simulando um passo do circuito
        tensoes_correntes = exemplo_2(degrau_amplitude, V2, ts, tmax, 1591.5, 1e-12)
        derivada_V2 = tensoes_correntes[2]
        ### Passo de integracao
        V2 = V2 + derivada_V2*ts # Euler

    plt.plot(vetor_tempo*1e3,vetor_saida)
    plt.title('Simulacao 2')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('V2 (V)')
    plt.show()

    
#####################################
#### Fim da definicao de funcoes ####
#####################################

simulacao_2()
