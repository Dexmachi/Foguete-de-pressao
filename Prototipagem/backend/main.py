import json
import numpy as np
from datetime import datetime
from movimento import calcular_movimento, haversine
from graficos import plotar_graficos
import sys
import os
import math


pasta_de_saida="json"
os.makedirs(pasta_de_saida, exist_ok=True)
arquivos_existentes = os.listdir(pasta_de_saida)
id_teste = len(arquivos_existentes) + 1


def process_data():
    print("Processando dados...")


    # Lê JSON Lines
    with open("dadosRecebidos.json", "r") as f:
        registros = json.load(f)
    
    

    # Ordena por data+hora
    registros.sort(
        key=lambda r: datetime.strptime(
            r["data"] + " " + r["hora"], "%d/%m/%Y %H:%M:%S"
        )
    )

    # Extrai tempos em segundos desde o primeiro ponto
    t0 = datetime.strptime(
        registros[0]["data"] + " " + registros[0]["hora"], "%d/%m/%Y %H:%M:%S"
    )
    tempos = np.array(
        [
            (
                datetime.strptime(r["data"] + " " + r["hora"], "%d/%m/%Y %H:%M:%S") - t0
            ).total_seconds()
            for r in registros
        ]
    )

    # Calcula distância acumulada em metros
    distancias = [0.0]
    for i in range(1, len(registros)):
        r0 = registros[i - 1]
        r1 = registros[i]
        d = haversine(r0["latitude"], r0["longitude"], r1["latitude"], r1["longitude"])
        distancias.append(distancias[-1] + d)
    distancias = np.array(distancias)

    # Verifica integridade
    if len(tempos) != len(distancias):
        print("Erro: número de tempos diferente de número de distâncias!")
        return

    # Calcula grandezas físicas
    resultados = calcular_movimento(tempos, distancias)
    with open("resultados.json", "r") as f:
        dados_para_distancia = json.load(f)
    
    distancia = int(dados_para_distancia.get("distancia", 0.0))
    
    with open("resultados.json", "w") as f:
        json.dump(
            {
                "velocidade_media": resultados["velocidade_media"],
                "aceleracao_media": resultados["aceleracao_media"],
                "distancia": distancia,
                "distancia_total": resultados["distancia_total"],
                "altura_maxima": resultados["altura_maxima"],
            }, f)
    
    
    data_teste = registros[0]["data"]
    data_formatada = datetime.strptime(data_teste, "%d/%m/%Y").strftime("%Y-%m-%d")
    nome_arquivo = f"{pasta_de_saida}/teste{id_teste}_{distancia}_Metros_{data_formatada}.json"
    with open(nome_arquivo, "w") as f:
        json.dump(registros, f, indent=4)
        
    

    # Exibe resultados
    print("\nResultados:")
    print(f"Velocidade média: {resultados['velocidade_media']:.2f} m/s")
    print(f"Aceleração média: {resultados['aceleracao_media']:.2f} m/s²")
    print(f"Distância total: {resultados['distancia_total']:.2f} metros")
    print(f"Arquivo salvo: {nome_arquivo}")
    print(f"Altura maáxima: {resultados['altura_maxima']:.2f} metros")

    # Plota gráficos
    plotar_graficos(tempos, distancias, resultados)

    # Abre o frontend novamente para mostrar os resultados
    # webbrowser.open('Frontend.html')


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--process":
        process_data()
    else:
        print("Modo padrão: executando análise")
        process_data()
