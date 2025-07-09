import json
import numpy as np
from datetime import datetime
from .movimento import calcular_movimento, haversine
from .graficos import plotar_graficos
import sys
import os


def gerar_mapa_trajetoria(registros, save_path):
    import folium

    # Extrai coordenadas
    coords = [(r["latitude"], r["longitude"]) for r in registros]
    if not coords:
        return

    # Centraliza o mapa no primeiro ponto
    m = folium.Map(location=coords[0], zoom_start=17)
    folium.PolyLine(coords, color="blue", weight=5, opacity=0.8).add_to(m)
    folium.Marker(coords[0], tooltip="Início", icon=folium.Icon(color="green")).add_to(
        m
    )
    folium.Marker(coords[-1], tooltip="Fim", icon=folium.Icon(color="red")).add_to(m)
    m.save(save_path)


def process_data():
    global VELOCIDADE_MEDIA
    print("Processando dados...")

    base_dir = os.path.dirname(os.path.dirname(__file__))
    dados_recebidos = os.path.join(base_dir, "data", "dadosRecebidos.json")
    static_dir = os.path.join(base_dir, "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Lê sempre do /data/dadosRecebidos.json na raiz do projeto
    with open(dados_recebidos, "r", encoding="utf-8") as f:
        registros = [json.loads(linha) for linha in f if linha.strip()]

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

    # Extrai as altitudes mandadas pelo BMP280
    altitudes_abs = [r["altitude"] for r in registros]  # lista de altitudes absolutas
    altitude_inicial = altitudes_abs[
        0
    ]  # usa a altitude do primeiro ponto como referência, ou seja, enquanto o foguete ainda não decolou
    alturas = [
        alt - altitude_inicial for alt in altitudes_abs
    ]  # subtrai a altitude inicial de todas as altitudes

    # Calcula grandezas físicas
    resultados = calcular_movimento(tempos, distancias)

    # Adiciona as altitudes aos resultados
    resultados["alturas"] = alturas

    # Exibe resultados
    print("\nResultados:")
    print(f"Velocidade média: {resultados['velocidade_media']:.2f} m/s")
    print(f"Aceleração média: {resultados['aceleracao_media']:.2f} m/s²")

    # Salva a velocidade média em um arquivo para o frontend
    with open(os.path.join(static_dir, "velocidade_media.txt"), "w") as f:
        f.write(str(resultados["velocidade_media"]))

    # Plota gráficos
    plotar_graficos(
        tempos,
        distancias,
        resultados,
        save_dir=static_dir,
    )

    # Gera o mapa da trajetória
    gerar_mapa_trajetoria(registros, os.path.join(static_dir, "trajetoria.html"))

    # Abre o frontend novamente para mostrar os resultados
    # webbrowser.open('Frontend.html')


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--process":
        process_data()
    else:
        print("Modo padrão: executando análise")
        process_data()
