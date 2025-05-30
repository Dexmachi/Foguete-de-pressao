import numpy as np
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula a distância em metros entre dois pontos na superfície da Terra
    especificados por latitude e longitude usando a fórmula de Haversine.

    Parâmetros:
        lat1, lon1: Latitude e longitude do primeiro ponto (em graus)
        lat2, lon2: Latitude e longitude do segundo ponto (em graus)

    Retorna:
        Distância entre os dois pontos em metros.
    """
    R = 6371e3  # raio da Terra em metros
    φ1, φ2 = radians(lat1), radians(lat2)  # converte latitudes para radianos
    Δφ = radians(lat2 - lat1)  # diferença de latitude em radianos
    Δλ = radians(lon2 - lon1)  # diferença de longitude em radianos

    # Fórmula de Haversine
    a = sin(Δφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # distância em metros


def calcular_espaco_tempo(
    data_points,
):  # Função que calcula o tempo (em segundos) e o espaço percorrido com base nos pontos GPS
    tempos = []  # Lista para armazenar os tempos convertidos
    espacos = [0]  # Primeira posição é zero, pois o deslocamento inicial é nulo S0 = 0
    total_espaco = 0  # Variável acumuladora do espaço percorrido

    for i, ponto in enumerate(data_points):  # Itera sobre os pontos de dados GPS
        ts = datetime.fromisoformat(
            ponto["timestamp"].replace("Z", "+00:00")
        )  # Converte timestamp ISO 8601 para datetime
        if (
            i > 0
        ):  # A partir do segundo ponto, calcula distância em relação ao ponto anterior
            anterior = data_points[i - 1]  # Ponto anterior
            d = haversine(  # Calcula distância entre os dois pontos (usando fórmula de Haversine)
                anterior["latitude"],
                anterior["longitude"],
                ponto["latitude"],
                ponto["longitude"],
            )
            total_espaco += d  # Soma a distância ao total
            espacos.append(total_espaco)  # Adiciona o novo valor ao vetor de espaço
        tempos.append(ts)  # Adiciona o timestamp à lista de tempos

    # Converter tempo para segundos desde o primeiro ponto
    tempo0 = tempos[0]  # Tempo inicial (referência)
    tempos_segundos = [
        (t - tempo0).total_seconds() for t in tempos
    ]  # Lista com tempos relativos em segundos

    return np.array(tempos_segundos), np.array(
        espacos
    )  # Retorna dois arrays: tempos e espaços


def calcular_movimento(
    tempos, espacos
):  # Função para calcular velocidades e acelerações a partir de tempos e espaços
    velocidades = np.diff(espacos) / np.diff(
        tempos
    )  # Calcula velocidades instantâneas (diferença do espaço / diferença do tempo)
    aceleracoes = np.diff(velocidades) / np.diff(
        tempos[:-1]
    )  # Calcula acelerações instantâneas (diferença da velocidade / diferença do tempo)

    velocidade_media = (espacos[-1] - espacos[0]) / (
        tempos[-1] - tempos[0]
    )  # Velocidade média total (deslocamento / tempo total)

    if len(velocidades) > 0:  # Se houver velocidades calculadas
        aceleracao_media = (velocidades[-1] - velocidades[0]) / (
            tempos[-1] - tempos[0]
        )  # Aceleração média total (variação da velocidade / tempo total)
    else:
        aceleracao_media = 0  # Caso não haja velocidades (ex: apenas um ponto), aceleração média é zero

    return {  # Retorna um dicionário com os resultados calculados
        "velocidades": velocidades,  # Array de velocidades instantâneas
        "aceleracoes": aceleracoes,  # Array de acelerações instantâneas
        "velocidade_media": velocidade_media,  # Valor da velocidade média total
        "aceleracao_media": aceleracao_media,  # Valor da aceleração média total
    }
