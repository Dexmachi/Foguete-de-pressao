import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plotar_graficos(tempos, espacos, resultados, save_dir="static"):
    df_espaco = pd.DataFrame({"Tempo": tempos, "Espaço": espacos})

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

    # Verifica se há aceleração
    tem_acel = len(resultados["aceleracoes"]) > 0

    if tem_acel:
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

    g = 9.8
    theta = np.radians(45)
    alcance = espacos[-1]
    if alcance > 0:
        v0 = np.sqrt(alcance * g / np.sin(2 * theta))
        v0y = v0 * np.sin(theta)
        tempos_np = np.array(tempos)
        altitudes = v0y * tempos_np - 0.5 * g * tempos_np**2
        altitudes[altitudes < 0] = 0
    else:
        altitudes = np.zeros_like(tempos)

    # --- Gráfico 1 e 2 (Espaço x Tempo + Velocidade x Tempo) ---
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    sns.lineplot(data=df_espaco, x="Tempo", y="Espaço", marker="o", ax=axs[0])
    axs[0].set_title("Espaço percorrido em função do tempo (m)")
    axs[0].set_xlabel("Tempo (s)")
    axs[0].set_ylabel("Espaço (m)")

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
    plt.savefig(f"{save_dir}/grafico_1_2.png")
    plt.close()

    # --- Gráfico 3 e 4 (Aceleração x Tempo e Trajetória física) ---
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico 3: aceleração ou espaço em branco se não houver
    if tem_acel:
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
        axs[0].set_xlabel("Tempo (s)")
        axs[0].set_ylabel("Aceleração (m/s²)")
    else:
        axs[0].text(
            0.5, 0.5, "Sem dados de aceleração", ha="center", va="center", fontsize=14
        )
        axs[0].axis("off")

    # Gráfico 4: Trajetória física (simulação)
    """
        Este gráfico é uma alternativa para a estimativa da altitude do foguete, ou seja, é uma simulação numérica baseada na dinâmica de projéteis, considerando a expansão adiabática do gás dentro da garrafa, o empuxo gerado pela saída da água pelo bocal, forças atuantes(empuxo, gravidade e efeito de perda da massa) e o movimento balístico do foguete após o esgotamento da água.
        
        Usado como base o arquivo para estimativa da trajetória do foguete encontrado no aprender.
        
        Será usada enquanto não tiver dados sobre a altitude real do foguete.
    
    """
    # Parâmetros necessários para a simulação
    p0 = 5e5  # Pressão inicial do tanque de água (Pa)
    pa = 1e5  # Pressão atmosférica ambiente (Pa)
    rho = 1000  # Densidade da água (kg/m³)
    V0 = 0.001  # Volume inicial da água no tanque (m³)
    Vg0 = 0.001  # Volume inicial do gás no tanque (m³)
    Ac = 0.002  # Área da câmara de compressão (m²)
    At = 0.0001  # Área da garganta do bocal (m²)
    theta0 = np.radians(45)  # Ângulo de lançamento (45 graus em radianos)
    me = 0.15  # Massa do foguete vazio (kg)
    gamma = 1.4  # Índice adiabático do gás (ar)
    dt = 0.01  # Passo de tempo da simulação (s)
    g = 9.81  # Aceleração da gravidade (m/s²)

    x, y = [0], [0]  # Listas de posições X e Y, inicializadas na origem
    v = (  # Velocidade inicial:
        resultados["velocidades"][0]
        if "velocidades" in resultados and len(resultados["velocidades"]) > 0
        else 0
    )  # Pega a primeira velocidade calculada, ou 0 se não houver

    Vg = Vg0  # Volume inicial do gás no tanque (m³) - variável para simulação
    V = V0  # Volume inicial da água no tanque (m³) - variável para simulação
    t = 0  # Tempo inicial da simulação (s)

    vx = v * np.cos(theta0)  # Componente horizontal da velocidade inicial
    vy = v * np.sin(theta0)  # Componente vertical da velocidade inicial

    while V > 0:  # Enquanto houver água no tanque (motor ligado)
        p = p0 * (Vg0 / Vg) ** gamma  # Pressão do gás após expansão adiabática
        delta_p = max(p - pa, 0)  # Diferença de pressão efetiva (sempre >= 0)
        ue = np.sqrt(
            2 * delta_p / (rho * (1 - (At / Ac) ** 2))
        )  # Velocidade de saída da água pelo bocal (m/s)
        m_dot = rho * At * ue  # Vazão mássica da água (kg/s)
        T = m_dot * ue  # Empuxo gerado (Newton)
        m = me + rho * V  # Massa total do foguete com água restante (kg)
        dv = (
            T / m - g * np.sin(theta0) - v * (m_dot / m)
        ) * dt  # Incremento da velocidade considerando forças
        v += dv  # Atualiza a velocidade do foguete
        dx = v * np.cos(theta0) * dt  # Incremento na posição horizontal
        dy = v * np.sin(theta0) * dt  # Incremento na posição vertical
        x.append(x[-1] + dx)  # Atualiza a posição X acumulada
        y.append(
            max(0, y[-1] + dy)
        )  # Atualiza posição Y, não deixando abaixo do chão (y=0)
        dV = m_dot * dt / rho  # Volume de água perdido no intervalo dt
        V -= dV  # Atualiza volume da água no tanque
        Vg += dV  # Atualiza volume do gás no tanque
        t += dt  # Incrementa o tempo da simulação

    vx = v * np.cos(theta0)  # Componente horizontal da velocidade ao fim do motor
    vy = v * np.sin(theta0)  # Componente vertical da velocidade ao fim do motor

    while y[-1] > 0:  # Enquanto o foguete estiver no ar (altura > 0)
        vy -= g * dt  # Atualiza velocidade vertical considerando a gravidade (queda)
        x.append(x[-1] + vx * dt)  # Atualiza posição horizontal
        y.append(
            max(0, y[-1] + vy * dt)
        )  # Atualiza posição vertical, mantendo ≥ 0 (chão)

    axs[1].plot(x, y, marker="o")
    axs[1].set_title("Trajetória física do foguete")
    axs[1].set_xlabel("Distância Horizontal (m)")
    axs[1].set_ylabel("Distância Vertical - Altitude (m)")

    plt.tight_layout()
    plt.savefig(f"{save_dir}/grafico_3_4.png")
    plt.close()
