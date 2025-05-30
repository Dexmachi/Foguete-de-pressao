import json
import numpy as np
from datetime import datetime
from movimento import calcular_movimento, haversine
from graficos import plotar_graficos
import sys
import webbrowser

def process_data():
    print("Processando dados...")
    
    # Lê JSON Lines
    with open('dadosRecebidos.json', 'r') as f:
        registros = json.load(f)

    # Ordena por data+hora
    registros.sort(key=lambda r: datetime.strptime(
        r['data'] + ' ' + r['hora'], "%d/%m/%Y %H:%M:%S"))

    # Extrai tempos em segundos desde o primeiro ponto
    t0 = datetime.strptime(
        registros[0]['data'] + ' ' + registros[0]['hora'], "%d/%m/%Y %H:%M:%S")
    tempos = np.array([(datetime.strptime(r['data'] + ' ' + r['hora'], "%d/%m/%Y %H:%M:%S") - t0).total_seconds()
                       for r in registros])

    # Calcula distância acumulada em metros
    distancias = [0.0]
    for i in range(1, len(registros)):
        r0 = registros[i-1]
        r1 = registros[i]
        d = haversine(r0['latitude'], r0['longitude'],
                      r1['latitude'], r1['longitude'])
        distancias.append(distancias[-1] + d)
    distancias = np.array(distancias)

    # Verifica integridade
    if len(tempos) != len(distancias):
        print("Erro: número de tempos diferente de número de distâncias!")
        return

    # Calcula grandezas físicas
    resultados = calcular_movimento(tempos, distancias)

    # Exibe resultados
    print("\nResultados:")
    print(f"Velocidade média: {resultados['velocidade_media']:.2f} m/s")
    print(f"Aceleração média: {resultados['aceleracao_media']:.2f} m/s²")

    # Plota gráficos
    plotar_graficos(tempos, distancias, resultados)
    
    # Abre o frontend novamente para mostrar os resultados
    webbrowser.open('Frontend.html')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--process':
        process_data()
    else:
        print("Modo padrão: executando análise")
        process_data()