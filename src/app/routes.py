from flask import Flask, request, jsonify, render_template, send_file
import datetime
import os
import logging
import json
from app.config import Config
from app import app
# from app.services.data_processing import save_data, process_data, gerar_mapa_trajetoria
from app.services.data_processing import save_data, process_data, gerar_mapa_trajetoria
import re
from app.movimento import calcular_espaco_tempo, calcular_movimento
from app.graficos import plot_graph_1_2, plot_graph_3_4




def get_next_launch_id():
    """Scans the data directory to find the next available launch ID."""
    data_dir = Config.DATA_DIR
    if not os.path.exists(data_dir):
        return 1

    max_id = 0
    for filename in os.listdir(data_dir):
        match = re.match(r"launch-data-(\d+)\.json", filename)
        if match:
            current_id = int(match.group(1))
            if current_id > max_id:
                max_id = current_id
    return max_id + 1


# Rota para a página inicial
@app.route("/")
def show_home_page():
    return render_template("Homepage.html")


# Rota para o histórico
@app.route("/history")
def show_history_page():
    return render_template("History.html")


# Rota para receber dados via POST
@app.post("/api/data")
def handle_data_post():
    if not Config.is_data_reception_active:
        return (
            jsonify(
                {"status": "error", "message": "Servidor não está aceitando dados"}
            ),
            503,
        )

    dados = request.get_json()
    if not dados:
        return jsonify({"status": "error", "message": "Dados inválidos"}), 400

    try:
        save_data(dados)
        hora_atual = datetime.datetime.now() - datetime.timedelta(hours=3)
        hora_recebimento = hora_atual.strftime("%H:%M:%S")
        logging.info("Dados recebidos: %s em %s", dados, hora_recebimento)
        return (
            jsonify({"status": "success", "message": "Dados recebidos com sucesso!"}),
            200,
        )
    except OSError as e:
        logging.exception("Erro ao salvar dados: %s", e)
        return jsonify({"status": "error", "message": "Erro ao salvar dados"}), 500


# Rota para iniciar o recebimento de dados
@app.post("/api/start-reception")
def activate_data_reception():
    Config.is_data_reception_active = True
    logging.info("Recepção de dados ativada.")
    return jsonify({"status": "success", "message": "Recepção de dados ativada!"}), 200


# Rota para parar o recebimento de dados
@app.post("/api/end-reception")
def deactivate_data_reception():
    Config.is_data_reception_active = False
    logging.info("Recepção de dados desativada.")
    return (
        jsonify({"status": "success", "message": "Servidor parou de receber dados!"}),
        200,
    )


# Rota para processar os dados
# @app.post("/api/process-data")
# def handle_process_data():
#     try:
#         req = request.get_json()
#         distancia = req.get("distancia")
#         print(distancia)

#         if distancia not in Config.VALID_DISTANCES:
#             logging.warning("Distância inválida: %s", distancia)
#             return jsonify({"status": "error", "message": "Distância inválida"}), 400

#         dados_destino_path = os.path.join(Config.DATA_DIR, f"dados{distancia}m.json")

#         try:
#             with open(Config.DADOS_RECEBIDOS_PATH, "r", encoding="utf-8") as f:
#                 linhas = f.readlines()
#         except FileNotFoundError:
#             logging.error("Arquivo de dados não encontrado.")
#             return (
#                 jsonify(
#                     {"status": "error", "message": "Arquivo de dados não encontrado."}
#                 ),
#                 404,
#             )

#         if not linhas or all(l.strip() == "" for l in linhas):
#             logging.warning("Nenhum dado para processar.")
#             return (
#                 jsonify({"status": "error", "message": "Nenhum dado para processar."}),
#                 400,
#             )

#         # Processa os dados (gera o gráfico)
#         logging.info("Iniciando processamento de dados...")

#         # Call the function directly and handle potential errors
#         try:
#             process_data(distancia)  # This will now run and save the velocity file
#         except Exception as e:
#             msg = f"Erro durante o processamento dos dados: {e}"
#             logging.exception(msg)
#             return jsonify({"status": "error", "message": msg}), 500

#         # --- This is the logic that was commented out, now active ---
#         # Depois de gerar o gráfico, move os dados para o arquivo de destino
#         try:
#             os.remove(Config.DADOS_RECEBIDOS_PATH)
#             with open(dados_destino_path, "a", encoding="utf-8") as f_dest:
#                 f_dest.writelines(linhas)
#             # Limpa o arquivo dadosRecebidos.json
#             # with open(Config.DADOS_RECEBIDOS_PATH, "w", encoding="utf-8") as f:
#             # f.write("")  # Limpa o arquivo escrevendo uma string vazia

#             # Lê a velocidade média do arquivo salvo
#             velocidade_media = 0.0
#             try:
#                 velocidade_media_path = os.path.join(
#                     Config.STATIC_DIR, "velocidade_media.txt"
#                 )
#                 with open(velocidade_media_path, "r") as f:
#                     velocidade_media = float(f.read().strip())
#             except FileNotFoundError:
#                 logging.warning(
#                     "Arquivo de velocidade_media não encontrado, usando 0.0"
#                 )
#             except Exception as e:
#                 logging.exception(f"Erro ao ler velocidade média: {e}")

#             logging.info(f"Velocidade média calculada: {velocidade_media}")
#             return (
#                 jsonify(
#                     {
#                         "status": "success",
#                         "velocity": velocidade_media,
#                     }
#                 ),
#                 200,
#             )

#         except Exception as e:
#             msg = f"Erro ao salvar/limpar dados: {e}"
#             logging.exception(msg)
#             return jsonify({"status": "error", "message": msg}), 500
#     except Exception as e:
#         msg = str(e)
#         logging.exception(msg)
#         return jsonify({"status": "error", "message": msg}), 500


# Rota para processar os dados
@app.post("/api/process-data")
def handle_process_data():
    try:
        # ... (code to get distancia) ...
        req = request.get_json()
        distancia = req.get("distancia")
        print(distancia)

        if distancia not in Config.VALID_DISTANCES:
            logging.warning("Distância inválida: %s", distancia)
            return jsonify({"status": "error", "message": "Distância inválida"}), 400

        # --- MODIFICATION START ---
        # 1. Get the next launch ID
        launch_id = get_next_launch_id()
        new_launch_file = os.path.join(Config.DATA_DIR, f"launch-data-{launch_id}.json")

        # 2. Rename the temporary launch file to its permanent, numbered name
        try:
            os.rename(Config.DADOS_RECEBIDOS_PATH, new_launch_file)
        except FileNotFoundError:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Nenhum dado de lançamento para processar.",
                    }
                ),
                404,
            )
        except Exception as e:
            return (
                jsonify({"status": "error", "message": f"Erro ao arquivar dados: {e}"}),
                500,
            )

        # 3. Process the newly created file
        process_data(new_launch_file)

        return (
            jsonify(
                {
                    "status": "success",
                    "launch_id": launch_id,  # Return the new ID to the frontend
                }
            ),
            200,
        )
        # --- MODIFICATION END ---

    except Exception as e:
        msg = str(e)
        logging.exception(msg)
        return jsonify({"status": "error", "message": msg}), 500


# @app.route('/graph/<string:graph_name>')
# def generate_graph(graph_name):


#     buffer = None

#     if graph_name == 'distance-vs-time':
#         print("gerando grafico de distancia em funcao do tempo")
#         buffer =




@app.route('/api/launch/<int:launch_id>/graph/<string:graph_name>.png')
def get_launch_graph(launch_id, graph_name):
    """Generates and returns a specific graph for a given launch."""
    launch_file = os.path.join(Config.DATA_DIR, f"launch-data-{launch_id}.json")
    if not os.path.exists(launch_file):
        return "Launch data not found", 404

    with open(launch_file, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f if line.strip()]

    tempos, espacos = calcular_espaco_tempo(data)
    
    # This is the incorrect altitude calculation, but we keep it for now to avoid breaking graficos.py
    # A proper fix would be to remove altitude plotting or use a real sensor.
    alturas = [r["latitude"] - data[0]["latitude"] for r in data]
    
    resultados = calcular_movimento(tempos, espacos)
    resultados["alturas"] = alturas

    buffer = None
    if graph_name == 'grafico_1_2':
        buffer = plot_graph_1_2(tempos, espacos, resultados)
    elif graph_name == 'grafico_3_4':
        buffer = plot_graph_3_4(tempos, espacos, resultados)
    else:
        return "Graph not found", 404

    return send_file(buffer, mimetype='image/png')






@app.route("/launch/<int:launch_id>")
def show_launch_details(launch_id):
    """Displays the analysis for a specific historical launch."""
    launch_file = os.path.join(Config.DATA_DIR, f"launch-data-{launch_id}.json")

    if not os.path.exists(launch_file):
        return "Lançamento não encontrado.", 404

    # Process the specific launch file to get the results dictionary
    resultados = process_data(launch_file)

    if resultados is None:
        return "Erro ao processar os dados do lançamento.", 500

    # Extract the specific float value for the template
    velocidade_media = resultados.get('velocidade_media', 0.0)

    return render_template(
        "Dashboard.html",
        launch_id=launch_id,
        velocity=velocidade_media,  # Pass the number, not the dictionary
        now=datetime.datetime.now().timestamp(),  # Cache buster for images
    )
