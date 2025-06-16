import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.movimento import calcular_espaco_tempo, haversine


def test_altitude_simples():
    # Simula pontos de GPS em linha reta (sem subida)
    pontos = [
        {
            "data": "01/01/2024",
            "hora": "10:00:00",
            "latitude": -23.0,
            "longitude": -46.0,
        },
        {
            "data": "01/01/2024",
            "hora": "10:00:01",
            "latitude": -23.0,
            "longitude": -46.0001,
        },
        {
            "data": "01/01/2024",
            "hora": "10:00:02",
            "latitude": -23.0,
            "longitude": -46.0002,
        },
    ]
    tempos, espacos = calcular_espaco_tempo(pontos)
    # O espaço deve aumentar, mas altitude (vertical) não é calculada diretamente do GPS 2D
    assert all(espacos[i] <= espacos[i + 1] for i in range(len(espacos) - 1))


def test_altitude_lancamento():
    # Simula subida e descida (trajetória de foguete idealizada)
    pontos = [
        {
            "data": "01/01/2024",
            "hora": "10:00:00",
            "latitude": -23.0,
            "longitude": -46.0,
        },
        {
            "data": "01/01/2024",
            "hora": "10:00:01",
            "latitude": -22.9999,
            "longitude": -46.0,
        },
        {
            "data": "01/01/2024",
            "hora": "10:00:02",
            "latitude": -22.9998,
            "longitude": -46.0,
        },
        {
            "data": "01/01/2024",
            "hora": "10:00:03",
            "latitude": -22.9999,
            "longitude": -46.0,
        },
        {
            "data": "01/01/2024",
            "hora": "10:00:04",
            "latitude": -23.0,
            "longitude": -46.0,
        },
    ]
    tempos, espacos = calcular_espaco_tempo(pontos)
    # O espaço total deve ser maior que zero
    assert espacos[-1] > 0


def test_distancia_zero():
    """Distância entre o mesmo ponto deve ser zero."""
    assert haversine(0.0, 0.0, 0.0, 0.0) == pytest.approx(0.0, abs=1e-6)


def test_distancia_equador():
    """
    Testa a distância entre dois pontos com 0.001 grau de longitude no equador.
    Esperado: ~111.32 metros.
    """
    lat1, lon1 = 0.0, 0.0
    lat2, lon2 = 0.0, 0.001

    distancia = haversine(lat1, lon1, lat2, lon2)
    assert distancia == pytest.approx(111.32, abs=1.0)


def test_distancia_sao_paulo_rio():
    """
    Testa a distância entre São Paulo e Rio de Janeiro.
    Esperado: aproximadamente 357 km.
    """
    sp_lat, sp_lon = -23.55052, -46.63331
    rj_lat, rj_lon = -22.90642, -43.18223

    distancia = haversine(sp_lat, sp_lon, rj_lat, rj_lon)
    assert distancia == pytest.approx(357000, abs=5000)  # ±5 km de tolerância


if __name__ == "__main__":
    pytest.main()
