# import matplotlib
# matplotlib.use('Agg')  # <-- ADD THIS LINE
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np


# def plotar_graficos(tempos, espacos, resultados, save_dir="static"):
#     df_espaco = pd.DataFrame({"Tempo": tempos, "Espaço": espacos})

#     df_velocidade = pd.DataFrame(
#         {
#             "Tempo": tempos[1:],
#             "Velocidade": resultados["velocidades"],
#             "Tipo": "Velocidade instantânea",
#         }
#     )

#     df_vel_media = pd.DataFrame(
#         {
#             "Tempo": [tempos[0], tempos[-1]],
#             "Velocidade": [resultados["velocidade_media"]] * 2,
#             "Tipo": "Velocidade média",
#         }
#     )

#     df_vel = pd.concat([df_velocidade, df_vel_media])

#     # Verifica se há aceleração
#     tem_acel = len(resultados["aceleracoes"]) > 0

#     if tem_acel:
#         df_aceleracao = pd.DataFrame(
#             {
#                 "Tempo": tempos[2:],
#                 "Aceleração": resultados["aceleracoes"],
#                 "Tipo": "Aceleração instantânea",
#             }
#         )
#         df_acel_media = pd.DataFrame(
#             {
#                 "Tempo": [tempos[0], tempos[-1]],
#                 "Aceleração": [resultados["aceleracao_media"]] * 2,
#                 "Tipo": "Aceleração média",
#             }
#         )
#         df_acel = pd.concat([df_aceleracao, df_acel_media])

#     g = 9.8
#     theta = np.radians(45)
#     alcance = espacos[-1]
#     if alcance > 0:
#         v0 = np.sqrt(alcance * g / np.sin(2 * theta))
#         v0y = v0 * np.sin(theta)
#         tempos_np = np.array(tempos)
#         altitudes = v0y * tempos_np - 0.5 * g * tempos_np**2
#         altitudes[altitudes < 0] = 0
#     else:
#         altitudes = np.zeros_like(tempos)

#     # --- Gráfico 1 e 2 (Espaço x Tempo + Velocidade x Tempo) ---
#     fig, axs = plt.subplots(1, 2, figsize=(12, 5))

#     sns.lineplot(data=df_espaco, x="Tempo", y="Espaço", marker="o", ax=axs[0])
#     axs[0].set_title("Distância percorrida em função do tempo (m)")
#     axs[0].set_xlabel("Tempo (s)")
#     axs[0].set_ylabel("Distância (m)")

#     sns.lineplot(
#         data=df_vel,
#         x="Tempo",
#         y="Velocidade",
#         hue="Tipo",
#         style="Tipo",
#         markers=True,
#         ax=axs[1],
#     )
#     axs[1].set_title("Velocidade em função do tempo (m/s)")
#     axs[1].set_xlabel("Tempo (s)")
#     axs[1].set_ylabel("Velocidade (m/s)")

#     plt.tight_layout()
#     plt.savefig(f"{save_dir}/grafico_1_2.png")
#     plt.close()

#     # --- Gráfico 3 e 4 (Aceleração x Tempo e Trajetória física) ---
#     fig, axs = plt.subplots(1, 2, figsize=(12, 5))

#     # Gráfico 3: aceleração ou espaço em branco se não houver
#     if tem_acel:
#         sns.lineplot(
#             data=df_acel,
#             x="Tempo",
#             y="Aceleração",
#             hue="Tipo",
#             style="Tipo",
#             markers=True,
#             ax=axs[0],
#         )
#         axs[0].set_title("Aceleração em função do tempo (m/s²)")
#         axs[0].set_xlabel("Tempo (s)")
#         axs[0].set_ylabel("Aceleração (m/s²)")
#     else:
#         axs[0].text(
#             0.5, 0.5, "Sem dados de aceleração", ha="center", va="center", fontsize=14
#         )
#         axs[0].axis("off")

#     # Gráfico 4: Trajetória física (Espaço x Altura real)
#     sns.lineplot(x=espacos, y=resultados["alturas"], marker="o", ax=axs[1])
#     axs[1].set_title("Trajetória do Foguete (Espaço x Altura Relativa)")
#     axs[1].set_xlabel("Distância Horizontal (m)")
#     axs[1].set_ylabel("Distância Vertical (m)")

#     plt.tight_layout()
#     plt.savefig(f"{save_dir}/grafico_3_4.png")
#     plt.close()


# import matplotlib
# matplotlib.use('Agg')
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
# import io

# def plotar_graficos(tempos, espacos, resultados):
#     """
#     Generates plot images and returns them as a dictionary of BytesIO buffers.
#     """
#     plots = {}

#     # --- Gráfico 1 e 2 (Espaço x Tempo + Velocidade x Tempo) ---
#     fig, axs = plt.subplots(1, 2, figsize=(12, 5))
#     # ... (existing code for plotting graph 1 & 2) ...
#     df_espaco = pd.DataFrame({"Tempo": tempos, "Espaço": espacos})

#     df_velocidade = pd.DataFrame(
#         {
#             "Tempo": tempos[1:],
#             "Velocidade": resultados["velocidades"],
#             "Tipo": "Velocidade instantânea",
#         }
#     )

#     df_vel_media = pd.DataFrame(
#         {
#             "Tempo": [tempos[0], tempos[-1]],
#             "Velocidade": [resultados["velocidade_media"]] * 2,
#             "Tipo": "Velocidade média",
#         }
#     )

#     df_vel = pd.concat([df_velocidade, df_vel_media])

#     sns.lineplot(data=df_espaco, x="Tempo", y="Espaço", marker="o", ax=axs[0])
#     axs[0].set_title("Distância percorrida em função do tempo (m)")
#     axs[0].set_xlabel("Tempo (s)")
#     axs[0].set_ylabel("Distância (m)")

#     sns.lineplot(
#         data=df_vel,
#         x="Tempo",
#         y="Velocidade",
#         hue="Tipo",
#         style="Tipo",
#         markers=True,
#         ax=axs[1],
#     )
#     axs[1].set_title("Velocidade em função do tempo (m/s)")
#     axs[1].set_xlabel("Tempo (s)")
#     axs[1].set_ylabel("Velocidade (m/s)")

#     plt.tight_layout()
#     buf1 = io.BytesIO()
#     plt.savefig(buf1, format='png')
#     buf1.seek(0)
#     plots['grafico_1_2'] = buf1
#     plt.close(fig)

#     # --- Gráfico 3 e 4 (Aceleração x Tempo e Trajetória física) ---
#     fig, axs = plt.subplots(1, 2, figsize=(12, 5))
#     # ... (existing code for plotting graph 3 & 4) ...
#     tem_acel = len(resultados["aceleracoes"]) > 0

#     if tem_acel:
#         df_aceleracao = pd.DataFrame(
#             {
#                 "Tempo": tempos[2:],
#                 "Aceleração": resultados["aceleracoes"],
#                 "Tipo": "Aceleração instantânea",
#             }
#         )
#         df_acel_media = pd.DataFrame(
#             {
#                 "Tempo": [tempos[0], tempos[-1]],
#                 "Aceleração": [resultados["aceleracao_media"]] * 2,
#                 "Tipo": "Aceleração média",
#             }
#         )
#         df_acel = pd.concat([df_aceleracao, df_acel_media])
#         sns.lineplot(
#             data=df_acel,
#             x="Tempo",
#             y="Aceleração",
#             hue="Tipo",
#             style="Tipo",
#             markers=True,
#             ax=axs[0],
#         )
#         axs[0].set_title("Aceleração em função do tempo (m/s²)")
#         axs[0].set_xlabel("Tempo (s)")
#         axs[0].set_ylabel("Aceleração (m/s²)")
#     else:
#         axs[0].text(0.5, 0.5, "Sem dados de aceleração", ha="center", va="center", fontsize=14)
#         axs[0].axis("off")

#     sns.lineplot(x=espacos, y=resultados["alturas"], marker="o", ax=axs[1])
#     axs[1].set_title("Trajetória do Foguete (Espaço x Altura Relativa)")
#     axs[1].set_xlabel("Distância Horizontal (m)")
#     axs[1].set_ylabel("Distância Vertical (m)")

#     plt.tight_layout()
#     buf2 = io.BytesIO()
#     plt.savefig(buf2, format='png')
#     buf2.seek(0)
#     plots['grafico_3_4'] = buf2
#     plt.close(fig)

#     return plots


import matplotlib

matplotlib.use("Agg")
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import io
import threading  # Import the threading module

# Create a global lock to make plotting thread-safe
plot_lock = threading.Lock()


def plot_graph_1_2(tempos, espacos, resultados):
    with plot_lock:
        """Generates the Distance vs. Time and Velocity vs. Time graph."""
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        # Plot 1: Distance vs Time
        df_espaco = pd.DataFrame({"Tempo": tempos, "Espaço": espacos})
        sns.lineplot(data=df_espaco, x="Tempo", y="Espaço", marker="o", ax=axs[0])
        axs[0].set_title("Distância percorrida em função do tempo (m)")
        axs[0].set_xlabel("Tempo (s)")
        axs[0].set_ylabel("Distância (m)")

        # Plot 2: Velocity vs Time
        df_velocidade = pd.DataFrame(
            {
                "Tempo": tempos[1:],
                "Velocidade": resultados["velocidades"],
                "Tipo": "Velocidade instantânea",
            }
        )
        df_vel_media = pd.DataFrame(
            {
                "Tempo": [tempos[0], tempos[-1]],
                "Velocidade": [resultados["velocidade_media"]] * 2,
                "Tipo": "Velocidade média",
            }
        )
        df_vel = pd.concat([df_velocidade, df_vel_media])
        sns.lineplot(
            data=df_vel,
            x="Tempo",
            y="Velocidade",
            hue="Tipo",
            style="Tipo",
            markers=True,
            ax=axs[1],
        )
        axs[1].set_title("Velocidade em função do tempo (m/s)")
        axs[1].set_xlabel("Tempo (s)")
        axs[1].set_ylabel("Velocidade (m/s)")

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf


def plot_graph_3_4(tempos, espacos, resultados):
    """Generates the Acceleration vs. Time and Trajectory graph."""
    with plot_lock:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        # Plot 3: Acceleration vs Time
        if len(resultados["aceleracoes"]) > 0:
            df_aceleracao = pd.DataFrame(
                {
                    "Tempo": tempos[2:],
                    "Aceleração": resultados["aceleracoes"],
                    "Tipo": "Aceleração instantânea",
                }
            )
            df_acel_media = pd.DataFrame(
                {
                    "Tempo": [tempos[0], tempos[-1]],
                    "Aceleração": [resultados["aceleracao_media"]] * 2,
                    "Tipo": "Aceleração média",
                }
            )
            df_acel = pd.concat([df_aceleracao, df_acel_media])
            sns.lineplot(
                data=df_acel,
                x="Tempo",
                y="Aceleração",
                hue="Tipo",
                style="Tipo",
                markers=True,
                ax=axs[0],
            )
            axs[0].set_title("Aceleração em função do tempo (m/s²)")
        else:
            axs[0].text(
                0.5,
                0.5,
                "Sem dados de aceleração",
                ha="center",
                va="center",
                fontsize=14,
            )
            axs[0].axis("off")

        # Plot 4: Trajectory
        sns.lineplot(x=espacos, y=resultados["alturas"], marker="o", ax=axs[1])
        axs[1].set_title("Trajetória do Foguete (Espaço x Altura Relativa)")
        axs[1].set_xlabel("Distância Horizontal (m)")
        axs[1].set_ylabel("Distância Vertical (m)")

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf
