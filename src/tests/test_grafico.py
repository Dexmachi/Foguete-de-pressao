import sys
import os
from pathlib import Path
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.graficos import plotar_graficos
from app.movimento import (
    calcular_movimento,
)  # Supondo que essa função esteja no módulo movimento


def test_grafico_altitude_tmp(tmp_path):
    tempos = np.linspace(0, 4, 9)
    espacos = np.array([0, 5, 15, 28, 40, 50, 58, 63, 65])
    resultados = calcular_movimento(tempos, espacos)

    save_dir = tmp_path
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    plotar_graficos(tempos, espacos, resultados, save_dir=str(save_dir))

    # Arquivos que esperamos
    arquivos_esperados = ["grafico_1_2.png", "grafico_3_4.png"]

    for nome_arquivo in arquivos_esperados:
        caminho = Path(save_dir) / nome_arquivo
        assert caminho.exists(), f"Arquivo {caminho} não foi criado"
