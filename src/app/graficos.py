import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plotar_graficos(
    tempos, espacos, resultados, save_path="static/grafico.png"
):  # Função para plotar gráficos com base nos dados de tempo, espaço e resultados
    df_espaco = pd.DataFrame(
        {"Tempo": tempos, "Espaço": espacos}
    )  # Cria DataFrame com os dados de espaço ao longo do tempo

    df_velocidade = pd.DataFrame(
        {  # Cria DataFrame com velocidades instantâneas
            "Tempo": tempos[
                1:
            ],  # Ignora o primeiro tempo (velocidade é calculada entre dois pontos)
            "Velocidade": resultados["velocidades"],  # Lista de velocidades calculadas
            "Tipo": "Velocidade instantânea",  # Rótulo para o gráfico
        }
    )

    df_vel_media = pd.DataFrame(
        {  # Cria DataFrame com a linha de velocidade média
            "Tempo": [tempos[0], tempos[-1]],  # Apenas dois tempos: início e fim
            "Velocidade": [resultados["velocidade_media"]]
            * 2,  # Mesmo valor para criar linha reta
            "Tipo": "Velocidade média",  # Rótulo para o gráfico
        }
    )

    df_vel = pd.concat(
        [df_velocidade, df_vel_media]
    )  # Junta os dois DataFrames de velocidade (instantânea e média)

    g = 9.8
    theta = np.radians(45)
    alcance = espacos[-1]  # distância total percorrida (horizontal)
    if alcance > 0:
        v0 = np.sqrt(alcance * g / np.sin(2 * theta))
        v0y = v0 * np.sin(theta)
        tempos_np = np.array(tempos)
        altitudes = v0y * tempos_np - 0.5 * g * tempos_np**2
        altitudes[altitudes < 0] = 0  # Não deixa altitude negativa
    else:
        altitudes = np.zeros_like(tempos)

    plt.figure(figsize=(20, 5))  # Ajusta o tamanho para 4 gráficos

    plt.subplot(1, 4, 1)  # Primeiro gráfico (posição 1 de 4)
    sns.lineplot(
        data=df_espaco, x="Tempo", y="Espaço", marker="o"
    )  # Plota espaço vs tempo com marcadores
    plt.title("Espaço percorrido em função do tempo (m)")  # Título do gráfico

    plt.subplot(1, 4, 2)  # Segundo gráfico (posição 2 de 4)
    sns.lineplot(
        data=df_vel, x="Tempo", y="Velocidade", hue="Tipo", style="Tipo", markers=True
    )  # Plota velocidades
    plt.title("Velocidade em função do tempo (m/s)")  # Título do gráfico

    if len(resultados["aceleracoes"]) > 0:  # Se houver dados de aceleração disponíveis
        df_aceleracao = pd.DataFrame(
            {  # Cria DataFrame com acelerações instantâneas
                "Tempo": tempos[
                    2:
                ],  # Começa do terceiro tempo (aceleração é derivada da velocidade, que é derivada do espaço)
                "Aceleração": resultados[
                    "aceleracoes"
                ],  # Lista de acelerações calculadas
                "Tipo": "Aceleração instantânea",  # Rótulo para o gráfico
            }
        )

        df_acel_media = pd.DataFrame(
            {  # Cria DataFrame com aceleração média
                "Tempo": [tempos[0], tempos[-1]],  # Do início ao fim
                "Aceleração": [resultados["aceleracao_media"]] * 2,  # Valor constante
                "Tipo": "Aceleração média",  # Rótulo para o gráfico
            }
        )

        df_acel = pd.concat(
            [df_aceleracao, df_acel_media]
        )  # Junta os dois DataFrames de aceleração

        plt.subplot(1, 4, 3)  # Terceiro gráfico (posição 3 de 4)
        sns.lineplot(
            data=df_acel,
            x="Tempo",
            y="Aceleração",
            hue="Tipo",
            style="Tipo",
            markers=True,
        )  # Plota acelerações
        plt.title("Aceleração em função do tempo (m/s²)")  # Título do gráfico

    # Gráfico de altitude estimada
    plt.subplot(1, 4, 4)  # Quarto gráfico (posição 4 de 4)
    plt.plot(tempos, altitudes, marker="o")  # Plota altitude vs tempo com marcadores
    plt.title("Altitude estimada em função do tempo (m)")  # Título do gráfico
    plt.xlabel("Tempo (s)")  # Rótulo do eixo x
    plt.ylabel("Altitude (m)")  # Rótulo do eixo y

    plt.tight_layout()
    plt.savefig(save_path)
