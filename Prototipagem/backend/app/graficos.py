import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

    sns.set_style("whitegrid")  # Define o estilo do gráfico com grade branca
    plt.figure(figsize=(15, 5))  # Define o tamanho da figura (largura x altura)

    plt.subplot(1, 3, 1)  # Primeiro gráfico (posição 1 de 3)
    sns.lineplot(
        data=df_espaco, x="Tempo", y="Espaço", marker="o"
    )  # Plota espaço vs tempo com marcadores
    plt.title("Espaço em função do tempo")  # Título do gráfico

    plt.subplot(1, 3, 2)  # Segundo gráfico (posição 2 de 3)
    sns.lineplot(
        data=df_vel, x="Tempo", y="Velocidade", hue="Tipo", style="Tipo", markers=True
    )  # Plota velocidades
    plt.title("Velocidade em função do tempo")  # Título do gráfico

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

        plt.subplot(1, 3, 3)  # Terceiro gráfico (posição 3 de 3)
        sns.lineplot(
            data=df_acel,
            x="Tempo",
            y="Aceleração",
            hue="Tipo",
            style="Tipo",
            markers=True,
        )  # Plota acelerações
        plt.title("Aceleração em função do tempo")  # Título do gráfico

    plt.tight_layout()
    plt.savefig(save_path)
