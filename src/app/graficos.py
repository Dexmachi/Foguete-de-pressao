import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plotar_graficos(tempos, espacos, resultados, save_path="static/grafico.png"):
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

    plt.figure(figsize=(30, 5))

    plt.subplot(1, 5, 1)
    sns.lineplot(data=df_espaco, x="Tempo", y="Espaço", marker="o")
    plt.title("Espaço percorrido em função do tempo (m)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Espaço (m)")

    plt.subplot(1, 5, 2)
    sns.lineplot(
        data=df_vel,
        x="Tempo",
        y="Velocidade",
        hue="Tipo",
        style="Tipo",
        markers=True,
    )
    plt.xlabel("Tempo (s)")
    plt.ylabel("Velocidade (m/s)")
    plt.title("Velocidade em função do tempo (m/s)")

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

        plt.subplot(1, 5, 3)
        sns.lineplot(
            data=df_acel,
            x="Tempo",
            y="Aceleração",
            hue="Tipo",
            style="Tipo",
            markers=True,
        )
        plt.xlabel("Tempo (s)")
        plt.ylabel("Aceleração (m/s²)")
        plt.title("Aceleração em função do tempo (m/s²)")

    plt.subplot(1, 5, 4)
    plt.plot(tempos, altitudes, marker="o")
    plt.title("Altitude estimada em função do tempo (m)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Altitude (m)")

    # === NOVO: Simulação física da trajetória ===

    # Parâmetros físicos do foguete (ajuste conforme o experimento real)
    p0 = 5e5  # Pressão inicial do ar dentro da garrafa (em Pascal) — ex: 5 atm
    pa = 1e5  # Pressão atmosférica (em Pascal) — geralmente 1 atm
    rho = 1000  # Densidade da água (kg/m³)
    V0 = 0.001  # Volume inicial de água (m³) — por exemplo, 1 litro
    Vg0 = 0.001  # Volume inicial do ar comprimido na garrafa (m³)
    Ac = 0.002  # Área da seção transversal da garrafa (m²) — raio ~2,5 cm
    At = 0.0001  # Área da tubeira (m²) — ex: diâmetro 1,1 cm
    theta0 = np.radians(45)  # Ângulo de lançamento convertido para radianos (45°)
    me = 0.15  # Massa da estrutura do foguete sem a água (kg)
    gamma = 1.4  # Expoente adiabático do ar (para expansão adiabática)
    dt = 0.01  # Passo de tempo da simulação (em segundos)

    # Inicializa listas para armazenar a trajetória horizontal (x) e vertical (y)
    x, y = [0], [0]

    # Usa a primeira velocidade registrada como velocidade inicial do foguete
    v = (
        resultados["velocidades"][0]
        if "velocidades" in resultados and len(resultados["velocidades"]) > 0
        else 0
    )

    Vg = Vg0  # Volume atual do ar comprimido
    V = V0  # Volume atual de água
    t = 0  # Tempo inicial da simulação

    # Decompõe a velocidade inicial em componentes horizontal e vertical
    vx = v * np.cos(theta0)
    vy = v * np.sin(theta0)

    # === Fase propulsiva (enquanto houver água no foguete) ===
    while V > 0:
        # Calcula a pressão interna no instante atual, considerando expansão adiabática
        p = p0 * (Vg0 / Vg) ** gamma
        delta_p = max(p - pa, 0)  # Diferença de pressão entre o interior e o exterior

        # Velocidade de exaustão da água usando Bernoulli + conservação da massa
        ue = np.sqrt(2 * delta_p / (rho * (1 - (At / Ac) ** 2)))

        # Vazão de massa da água que está saindo (kg/s)
        m_dot = rho * At * ue

        # Empuxo gerado pela água sendo ejetada
        T = m_dot * ue

        # Massa total atual do foguete (estrutura + água restante)
        m = me + rho * V

        # Calcula variação da velocidade com base no empuxo, gravidade e perda de massa
        dv = (T / m - g * np.sin(theta0) - v * (m_dot / m)) * dt
        v += dv  # Atualiza velocidade escalar

        # Calcula deslocamento horizontal e vertical no intervalo de tempo dt
        dx = v * np.cos(theta0) * dt
        dy = v * np.sin(theta0) * dt

        # Atualiza posições horizontal e vertical
        x.append(x[-1] + dx)
        y.append(max(0, y[-1] + dy))  # Garante que y nunca fique negativo

        # Atualiza volume de água e volume de ar após ejeção
        dV = m_dot * dt / rho
        V -= dV
        Vg += dV

        # Atualiza tempo
        t += dt

    # === Fase balística (após a queima, movimento parabólico) ===

    # Recalcula componentes da velocidade no fim da fase propulsiva
    vx = v * np.cos(theta0)
    vy = v * np.sin(theta0)

    # Continua a simulação até o foguete tocar o chão (y <= 0)
    while y[-1] > 0:
        vy -= g * dt  # Apenas a gravidade atua no eixo vertical
        x.append(x[-1] + vx * dt)  # Deslocamento horizontal constante
        y.append(max(0, y[-1] + vy * dt))  # Deslocamento vertical com gravidade

    # Plot da trajetória real
    plt.subplot(1, 5, 5)
    plt.plot(x, y, marker="o")
    plt.title("Trajetória física do foguete")
    plt.xlabel("Distância Horizontal (m)")
    plt.ylabel("Distância Vertical - Altitude (m)")

    plt.tight_layout()
    plt.savefig(save_path)
