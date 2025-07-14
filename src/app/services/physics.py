from app.config import Config
import logging
import os
import numpy as np
import json
from datetime import datetime
import csv
#from app.movimento import calcular_movimento
#from app.graficos import plotar_graficos
from math import radians, sin, cos, sqrt, atan2


def calculate_times(data):
    initial_timestamp = datetime.strptime(
        data[0]["data"] + " " + data[0]["hora"], "%d/%m/%Y %H:%M:%S"
    )

    seconds_list = [
        (
            datetime.strptime(i["data"] + " " + i["hora"], "%d/%m/%Y %H:%M:%S")
            - initial_timestamp
        ).total_seconds()
        for i in data
    ]
    return np.array(seconds_list)


def calculate_distances(data):
    distances_m = [0.0]
    for i in range(1, len(data)):
        r0 = data[i - 1]
        r1 = data[i]
        d = haversine(r0["latitude"], r0["longitude"], r1["latitude"], r1["longitude"])
        distances_m.append(distances_m[-1] + d)
    return np.array(distances_m)


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
