from flask import Flask, request, jsonify, render_template, send_from_directory
import datetime
import json
import os
import subprocess
import signal
import sys
import logging
from flask_cors import CORS
import csv

# Configuração do logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Variável para controlar se o servidor está aceitando dados
RECEBA_DADOS = False

# Configuração de diretórios
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_DIR_SAVE = os.path.join(BASE_DIR, "data/dadosSalvos")
dados_selecionados_path = os.path.join(DATA_DIR, "dados10m.json")
dados_recebidos_path = os.path.join(DATA_DIR, "dadosRecebidos.json")
# Inicialização da aplicação Flask
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
CORS(app)


# Rota para receber dados via POST

@app.route("/settarTeste", methods=["POST"])
def settar_teste():
        try:
            dados_recebidos_path = os.path.join(DATA_DIR, "dadosRecebidos.json")
            dados_destino_path = os.path.join(DATA_DIR_SAVE, "dados(1)_10M_16-06-2025.json")

            with open(dados_destino_path, "r", encoding="utf-8") as f_dest:
                conteudo = f_dest.readlines()

            with open(dados_recebidos_path, "w", encoding="utf-8") as f:
                f.writelines(conteudo)

            return jsonify({"status": "success", "message": "Dados carregados com sucesso"}), 200

        except Exception as e:
            logging.exception("Erro ao settar teste")
            return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/gps", methods=["POST"])
def receber_dados():
    if not RECEBA_DADOS:
        return (
            jsonify(
                {"status": "error", "mensagem": "Servidor não está aceitando dados"}
            ),
            503,
        )

    dados = request.get_json()
    if not dados:
        return jsonify({"status": "error", "mensagem": "Dados inválidos"}), 400

    try:
        save_data(dados)
        hora_atual = datetime.datetime.now() - datetime.timedelta(hours=3)
        hora_recebimento = hora_atual.strftime("%H:%M:%S")
        logging.info(f"Dados recebidos: {dados} em {hora_recebimento}")
        return (
            jsonify({"status": "ok", "mensagem": "Dados recebidos com sucesso!"}),
            200,
        )
    except Exception as e:
        logging.exception(f"Erro ao salvar dados: {e}")
        return jsonify({"status": "error", "mensagem": "Erro ao salvar dados"}), 500


# Rota para a página inicial
@app.route("/")
def index():
    return render_template("Frontend.html")


# Rota para iniciar o servidor
@app.route("/start-server", methods=["POST"])
def start_server_route():
    global RECEBA_DADOS
    RECEBA_DADOS = True
    logging.info("Servidor iniciado")
    return jsonify({"status": "success", "message": "Servidor iniciado"}), 200


# Rota para o histórico
@app.route("/historico")
def historico():
    return send_from_directory(BASE_DIR, "templates/historico.html")


# Rota para arquivos estáticos
@app.route("/static/<path:filename>")
def static_files(filename):
    try:
        return send_from_directory(STATIC_DIR, filename)
    except Exception as e:
        logging.error(f"Erro ao servir arquivo estático {filename}: {e}")
        return jsonify({"error": "File not found"}), 404


# Rota para parar o servidor
@app.route("/stop-server", methods=["POST"])
def stop_server_route():
    global RECEBA_DADOS
    RECEBA_DADOS = False
    logging.info("Servidor parado")
    return (
        jsonify({"status": "success", "message": "Servidor parou de receber dados!"}),
        200,
    )


# Rota para processar os dados
@app.route("/process-data", methods=["POST"])
def process_data():
    try:
        req = request.get_json()
        distancia = req.get("distancia")

        # =============inicio da criação do histórico=============
        temp = []
        with open(os.path.join(DATA_DIR, "dadosRecebidos.json"), "r", encoding="utf-8") as f:
            for linha in f:
                temp.append(json.loads(linha))
        
        data = temp[0]["data"].replace("/", "-")
        
        idT = len(os.listdir(DATA_DIR_SAVE))+1

        if distancia not in [10, 20, 30]:
            logging.warning(f"Distância inválida: {distancia}")
            return jsonify({"status": "error", "message": "Distância inválida"}), 400

        dados_recebidos_path = os.path.join(DATA_DIR, "dadosRecebidos.json")
        dados_destino_path = os.path.join(DATA_DIR_SAVE, f"dados({idT})_{distancia}M_{data}.json")

        # =============fim da criação do histórico=============

        try:
            with open(dados_recebidos_path, "r", encoding="utf-8") as f:
                linhas = f.readlines()
        except FileNotFoundError:
            msg = "Arquivo de dados não encontrado."
            logging.error(msg)
            return jsonify({"status": "error", "message": msg}), 404

        if not linhas or all(l.strip() == "" for l in linhas):
            msg = "Nenhum dado para processar."
            logging.warning(msg)
            return jsonify({"status": "error", "message": msg}), 400

        # Processa os dados (gera o gráfico)
        logging.info("Iniciando subprocesso para gerar gráfico")
        main_py_path = os.path.join(BASE_DIR, "app", "main.py")
        result = subprocess.run(
            ["python", main_py_path, "--process"], capture_output=True, text=True
        )

        if result.returncode == 0:
            # Depois de gerar o gráfico, move os dados para o arquivo de destino
            try:
                with open(dados_destino_path, "a", encoding="utf-8") as f_dest:
                    f_dest.writelines(linhas)
                # Limpa o arquivo dadosRecebidos.json
                with open(dados_recebidos_path, "w", encoding="utf-8") as f:
                    f.write("")  # Limpa o arquivo escrevendo uma string vazia

                # Lê a velocidade média do arquivo salvo
                try:
                    velocidade_media_path = os.path.join(
                        STATIC_DIR, "velocidade_media.txt"
                    )
                    with open(velocidade_media_path, "r") as f:
                        velocidade_media = float(f.read().strip())
                except FileNotFoundError:
                    velocidade_media = 0.0
                    logging.warning(
                        "Arquivo de velocidade_media não encontrado, usando 0.0"
                    )
                except Exception as e:
                    velocidade_media = 0.0
                    logging.exception(f"Erro ao ler velocidade média: {e}")

                logging.info(f"Velocidade média calculada: {velocidade_media}")
                return (
                    jsonify(
                        {
                            "status": "success",
                            "velocity": velocidade_media,
                        }
                    ),
                    200,
                )
            except Exception as e:
                msg = f"Erro ao salvar/limpar dados: {e}"
                logging.exception(msg)
                return jsonify({"status": "error", "message": msg}), 500
        else:
            msg = f"Erro no subprocesso: {result.stderr}"
            logging.error(msg)
            return jsonify({"status": "error", "message": msg}), 500

    except Exception as e:
        msg = str(e)
        logging.exception(msg)
        return jsonify({"status": "error", "message": msg}), 500

@app.route("/dadosHistorico", methods=["POST"])
def dados_historico():
    try:
        dados_recebidos_path = os.path.join(DATA_DIR, "dadosRecebidos.json")


        try:
            with open(dados_recebidos_path, "r", encoding="utf-8") as f:
                linhas = f.readlines()
        except FileNotFoundError:
            msg = "Arquivo de dados não encontrado."
            logging.error(msg)
            return jsonify({"status": "error", "message": msg}), 404

        if not linhas or all(l.strip() == "" for l in linhas):
            msg = "Nenhum dado para processar."
            logging.warning(msg)
            return jsonify({"status": "error", "message": msg}), 400

        # Processa os dados (gera o gráfico)
        logging.info("Iniciando subprocesso para gerar gráfico")
        main_py_path = os.path.join(BASE_DIR, "app", "main.py")
        result = subprocess.run(
            ["python", main_py_path, "--process"], capture_output=True, text=True
        )

        if result.returncode == 0:
            # Depois de gerar o gráfico, exclui os dados do arquivo de destino
            try:
                # Limpa o arquivo dadosRecebidos.json
                with open(dados_recebidos_path, "w", encoding="utf-8") as f:
                    f.write("")  # Limpa o arquivo escrevendo uma string vazia

                # Lê a velocidade média do arquivo salvo
                try:
                    velocidade_media_path = os.path.join(
                        STATIC_DIR, "velocidade_media.txt"
                    )
                    with open(velocidade_media_path, "r") as f:
                        velocidade_media = float(f.read().strip())
                except FileNotFoundError:
                    velocidade_media = 0.0
                    logging.warning(
                        "Arquivo de velocidade_media não encontrado, usando 0.0"
                    )
                except Exception as e:
                    velocidade_media = 0.0
                    logging.exception(f"Erro ao ler velocidade média: {e}")

                logging.info(f"Velocidade média calculada: {velocidade_media}")
                return (
                    jsonify(
                        {
                            "status": "success",
                            "velocity": velocidade_media,
                        }
                    ),
                    200,
                )
            except Exception as e:
                msg = f"Erro ao salvar/limpar dados: {e}"
                logging.exception(msg)
                return jsonify({"status": "error", "message": msg}), 500
        else:
            msg = f"Erro no subprocesso: {result.stderr}"
            logging.error(msg)
            return jsonify({"status": "error", "message": msg}), 500

    except Exception as e:
        msg = str(e)
        logging.exception(msg)
        return jsonify({"status": "error", "message": msg}), 500
    
    


# Função para salvar os dados
def save_data(data):
    dados_recebidos_path = os.path.join(DATA_DIR, "dadosRecebidos.json")
    dados_brutos_path = os.path.join(DATA_DIR, "dados_brutos.csv")
    try:
        with open(dados_recebidos_path, "a", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

        # Salvar dados brutos em CSV
        with open(dados_brutos_path, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Escrever cabeçalho se o arquivo estiver vazio
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(data)

    except Exception as e:
        logging.error(f"Erro ao salvar dados em arquivo: {e}")


# Funções para iniciar e parar o servidor
def start_server():
    app.run(host="0.0.0.0", port=5000)


def stop_server():
    global RECEBA_DADOS
    RECEBA_DADOS = False
    logging.info("Servidor sendo parado...")
    os.kill(os.getpid(), signal.SIGINT)


# Inicialização do servidor
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--start":
        print("Iniciando servidor...")
        start_server()
    elif len(sys.argv) > 1 and sys.argv[1] == "--stop":
        print("Parando servidor...")
        stop_server()
    else:
        print("Modo padrão: executando como servidor")
        start_server()
