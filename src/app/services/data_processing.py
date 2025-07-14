from app.config import Config
import logging
import os
import numpy as np
import json
from datetime import datetime
import csv
from app.movimento import calcular_movimento
from app.services.physics import calculate_times, calculate_distances


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


# Função para salvar os dados
def save_data(data):
    try:
        # Salvar dados brutos em JSON
        with open(Config.DADOS_RECEBIDOS_PATH, "a", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")
    except (IOError, OSError, json.JSONDecodeError) as e:
        logging.error("Erro ao salvar dados em arquivo: %s", e)


# def process_data(selectedDistance):
#     global VELOCIDADE_MEDIA
#     print("Processando dados...")

#     # base_dir = os.path.dirname(os.path.dirname(__file__))
#     # dados_recebidos = os.path.join(base_dir, "data", "dadosRecebidos.json")
#     # static_dir = os.path.join(base_dir, "app", "static")
#     if not os.path.exists(Config.STATIC_DIR):
#         os.makedirs(Config.STATIC_DIR)

#     # Lê sempre do /data/launch-data.json na raiz do projeto
#     with open(Config.DADOS_RECEBIDOS_PATH, "r", encoding="utf-8") as f:
#         data = [json.loads(linha) for linha in f if linha.strip()]
#         # print(data) IMPORTANTE =============================================================================================================

#     # Ordena por data+hora
#     data.sort(
#         key=lambda r: datetime.strptime(
#             r["data"] + " " + r["hora"], "%d/%m/%Y %H:%M:%S"
#         )
#     )

#     times = calculate_times(data)
#     distances = calculate_distances(data)

#     # Verifica integridade
#     if len(times) != len(distances):
#         print("Erro: número de tempos diferente de número de distâncias!")
#         return

#     # Extrai as altitudes mandadas pelo BMP280
#     altitudes_abs = [r["latitude"] for r in data]  # lista de altitudes absolutas
#     altitude_inicial = altitudes_abs[
#         0
#     ]  # usa a altitude do primeiro ponto como referência, ou seja, enquanto o foguete ainda não decolou
#     alturas = [
#         alt - altitude_inicial for alt in altitudes_abs
#     ]  # subtrai a altitude inicial de todas as altitudes

#     # Calcula grandezas físicas
#     resultados = calcular_movimento(times, distances)

#     # Adiciona as altitudes aos resultados
#     resultados["alturas"] = alturas

#     # Exibe resultados
#     print("\nResultados:")
#     print(f"Velocidade média: {resultados['velocidade_media']:.2f} m/s")
#     print(f"Aceleração média: {resultados['aceleracao_media']:.2f} m/s²")

#     # Salva a velocidade média em um arquivo para o frontend
#     with open(os.path.join(Config.STATIC_DIR, "velocidade_media.txt"), "w") as f:
#         f.write(str(resultados["velocidade_media"]))

#     # Plota gráficos
#     plotar_graficos(
#         times,
#         distances,
#         resultados,
#         save_dir=Config.STATIC_DIR,
#     )

#     # Gera o mapa da trajetória
#     gerar_mapa_trajetoria(data, os.path.join(Config.STATIC_DIR, "trajetoria.html"))

#     # Abre o frontend novamente para mostrar os resultados
#     # webbrowser.open('Frontend.html')


def process_data(launch_file_path):
    print(f"Processando dados de: {launch_file_path}")

    # Lê do arquivo de lançamento especificado
    with open(launch_file_path, "r", encoding="utf-8") as f:
        data = [json.loads(linha) for linha in f if linha.strip()]

    if not data:
        print("Erro: Arquivo de lançamento está vazio.")
        return None

    # Ordena por data+hora
    data.sort(
        key=lambda r: datetime.strptime(
            r["data"] + " " + r["hora"], "%d/%m/%Y %H:%M:%S"
        )
    )

    times = calculate_times(data)
    distances = calculate_distances(data)

    # Verifica integridade
    if len(times) != len(distances):
        print("Erro: número de tempos diferente de número de distâncias!")
        return None

    # This altitude calculation is incorrect, but we keep it for the graph
    altitudes_abs = [r["latitude"] for r in data]
    altitude_inicial = altitudes_abs[0]
    alturas = [alt - altitude_inicial for alt in altitudes_abs]

    # Calcula grandezas físicas
    resultados = calcular_movimento(times, distances)
    resultados["alturas"] = alturas
    resultados["data"] = data  # Pass the raw data through as well

    # Exibe resultados no console do servidor
    print(f"Velocidade média: {resultados['velocidade_media']:.2f} m/s")

    # REMOVED: Saving velocidade_media.txt
    # REMOVED: Calling plotar_graficos()
    # REMOVED: Calling gerar_mapa_trajetoria()

    # Return the entire dictionary of results
    print(resultados)
    return resultados
