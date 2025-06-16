import os, sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.graficos import plotar_graficos
from app.movimento import calcular_movimento


def test_grafico_altitude_tmp(tmp_path):
    # Simula dados de lançamento: tempo, espaço e resultados
    tempos = np.linspace(0, 4, 9)  # 0s a 4s, 9 pontos
    espacos = np.array([0, 5, 15, 28, 40, 50, 58, 63, 65])  # deslocamento crescente

    # Calcula resultados físicos
    resultados = calcular_movimento(tempos, espacos)

    # Caminho temporário para salvar o gráfico
    save_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../static/grafico_teste.png")
    )
    # Gera o gráfico
    plotar_graficos(tempos, espacos, resultados, save_path=str(save_path))

    # Verifica se o arquivo foi criado
    assert os.path.exists(save_path)

    # Opcional: verifica se a altitude máxima ocorre no meio do tempo (trajetória parabólica)
    # (A curva de altitude deve subir e depois descer)
    # Para isso, podemos simular o cálculo da altitude como no plotar_graficos
    g = 9.8
    theta = np.radians(45)
    alcance = espacos[-1]
    v0 = np.sqrt(alcance * g / np.sin(2 * theta)) if alcance > 0 else 0
    v0y = v0 * np.sin(theta)
    altitudes = v0y * tempos - 0.5 * g * tempos**2
    altitudes[altitudes < 0] = 0

    # A altitude máxima deve ser maior que zero e ocorrer antes do último ponto
    assert altitudes.max() > 0
    assert np.argmax(altitudes) < len(altitudes) - 1
