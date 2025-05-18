from movimento import calcular_movimento, calcular_espaco_tempo
from graficos import plotar_graficos
import numpy as np
import json


def main():
    print("Programa de Análise de Movimento")
    print("Lendo dados de movimento do arquivo JSON...")

    with open('ficticio.json', 'r') as f:
        dados = json.load(f)
    
    data_points = dados['data_points']
    tempos, espacos = calcular_espaco_tempo(data_points)
    
    if len(tempos) != len(espacos):
        print("Erro: O número de tempos deve ser igual ao número de espaços!")
        return
    # Entrada de dados
    #tempos = input("Tempos (ex: 0,1,2,3,4): ").split(',')
    #espacos = input("Espaços percorridos (ex: 0,2,8,18,32): ").split(',')

    # Convertendo para arrays numéricos
    #tempos = np.array([float(t) for t in tempos])
    #espacos = np.array([float(e) for e in espacos])

    

    # Calculando as grandezas físicas
    resultados = calcular_movimento(tempos, espacos)

    # Exibindo resultados numéricos
    print("\nResultados:")
    print(f"Velocidade média: {resultados['velocidade_media']:.2f} m/s")
    print(f"Aceleração média: {resultados['aceleracao_media']:.2f} m/s²")

    # Plotando gráficos
    plotar_graficos(tempos, espacos, resultados)
    
if __name__ == "__main__":
    main()