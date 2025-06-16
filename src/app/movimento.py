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


def calcular_espaco_tempo(data_points):
    """
    Calcula o tempo (em segundos) e o espaço percorrido com base nos pontos GPS.
    Aceita lista de dicionários com 'data'+'hora' ou 'timestamp', 'latitude', 'longitude'.

    Parâmetros:
        data_points: Lista de dicionários contendo os pontos GPS com informações de tempo.

    Retorna:
        Dois arrays NumPy: um com os tempos em segundos e outro com os espaços percorridos.
    """
    tempos = []  # Lista para armazenar os tempos convertidos
    espacos = [
        0.0
    ]  # Primeira posição é zero, pois o deslocamento inicial é nulo S0 = 0
    total_espaco = 0.0  # Variável acumuladora do espaço percorrido

    if not data_points:  # Se não houver pontos de dados, retorna arrays vazios
        return np.array([]), np.array([])

    for i, ponto in enumerate(data_points):  # Itera sobre os pontos de dados GPS
        # Suporte a 'timestamp' ou 'data'+'hora'
        if "timestamp" in ponto:
            ts = datetime.fromisoformat(
                ponto["timestamp"].replace("Z", "+00:00")
            )  # Converte timestamp ISO 8601 para datetime
        elif "data" in ponto and "hora" in ponto:
            ts = datetime.strptime(
                f"{ponto['data']} {ponto['hora']}", "%d/%m/%Y %H:%M:%S"
            )  # Converte data e hora separadas para datetime
        else:
            raise ValueError("Ponto sem campo de tempo reconhecido")

        if (
            i > 0
        ):  # A partir do segundo ponto, calcula distância em relação ao ponto anterior
            anterior = data_points[i - 1]  # Ponto anterior
            d = haversine(  # Calcula distância entre os dois pontos (usando fórmula de Haversine)
                float(anterior["latitude"]),
                float(anterior["longitude"]),
                float(ponto["latitude"]),
                float(ponto["longitude"]),
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


def calcular_movimento(tempos, espacos):
    """
    Calcula velocidades e acelerações instantâneas, além de médias, a partir de arrays de tempo e espaço.
    Parâmetros:
        tempos: array NumPy de tempos (em segundos)
        espacos: array NumPy de posições (em metros)
    Retorna:
        dict com arrays de velocidades, acelerações, velocidade média e aceleração média
    """
    # Protege contra entradas inválidas
    if len(tempos) < 2 or len(espacos) < 2:
        return {
            "velocidades": np.array([]),
            "aceleracoes": np.array([]),
            "velocidade_media": 0.0,
            "aceleracao_media": 0.0,
        }

    # Calcula diferenças de tempo e espaço
    delta_t = np.diff(tempos)
    delta_s = np.diff(espacos)

    # Evita divisão por zero
    delta_t[delta_t == 0] = 1e-9

    velocidades = delta_s / delta_t

    # Aceleração só faz sentido se houver pelo menos 2 velocidades
    if len(velocidades) > 1:
        delta_tv = np.diff(tempos[:-1])
        delta_tv[delta_tv == 0] = 1e-9
        aceleracoes = np.diff(velocidades) / delta_tv
    else:
        aceleracoes = np.array([])

    velocidade_media = (
        (espacos[-1] - espacos[0]) / (tempos[-1] - tempos[0])
        if (tempos[-1] - tempos[0]) != 0
        else 0.0
    )

    if len(velocidades) > 1 and (tempos[-1] - tempos[0]) != 0:
        aceleracao_media = (velocidades[-1] - velocidades[0]) / (tempos[-1] - tempos[0])
    else:
        aceleracao_media = 0.0

    return {
        "velocidades": velocidades,
        "aceleracoes": aceleracoes,
        "velocidade_media": velocidade_media,
        "aceleracao_media": aceleracao_media,
    }
