from flask import Flask, request, jsonify, render_template, send_from_directory
import datetime
import json
import sys
import signal
import os
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/start-server": {
            "origins": ["http://127.0.0.1:5000", "http://localhost:5000"]
        },
        r"/gps": {"origins": "*"},
        r"/ping": {"origins": "*"},
        r"/save-distance": {"origins": ["http://127.0.0.1:5000", "http://localhost:5000"]},
    },
)


def save_data(data):
    with open("dadosRecebidos.json", "a", encoding="utf-8") as f:
        json.dump(data, f)
        f.write("\n")


@app.route("/gps", methods=["POST"])
def receber_dados():
    dados = request.json
    save_data(dados)
    hora_atual = datetime.datetime.now() - datetime.timedelta(hours=3)
    hora_recebimento = hora_atual.strftime("%H:%M:%S")
    print(f"[{hora_recebimento}] Dados recebidos: {dados}")
    return jsonify({"status": "ok", "mensagem": "Dados recebidos com sucesso!"})


@app.route("/")
def index():
    return render_template("Frontend.html")


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "mensagem": "pong"})


@app.route("/start-server", methods=["GET", "POST", "OPTIONS"])
def start_server_route():
    if request.method == "OPTIONS":
        # Handle preflight request
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    return jsonify({"status": "success", "message": "Server started"})

@app.route("/historico")  # <-- Adicione esta rota
def historico():
    return send_from_directory(".", "templates/historico.html")

@app.route("/save-distance", methods=["POST"])
def save_distance():
    try:
        data = request.get_json()
        if "distancia" not in data:
            print("[ERRO] Chave 'distancia' não está no JSON")
            return jsonify({"status": "error", "message": "Distância não fornecida"}), 400
        
        distancia = data["distancia"]

        with open("resultados.json", "r") as f:
            dados_anteriores = json.load(f)

        dados_anteriores["distancia"] = distancia

        
        with open("resultados.json", "w") as f:
            json.dump(dados_anteriores, f, indent=4)

        print("[INFO] Distância salva:", distancia)
        return jsonify({"status": "success", "message": "Distância salva com sucesso!"})
    except Exception as e:
        print("[ERRO] Exceção no save_distance:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/process-data', methods=['POST'])
def process_data():
    try:
        result = subprocess.run(
            ["python", "main.py", "--process"], capture_output=True, text=True
        )

        if result.returncode == 0:
            with open("resultados.json", "r") as f:
                    resultados = json.load(f)
                    velocidade_media = float(resultados.get("velocidade_media", 0.0))
                    distancia_total = float(resultados.get("distancia_total", 0.0))
                    altura_maxima = float(resultados.get("altura_maxima", 0.0))
            return jsonify(
                {
                    "status": "success",
                    "velocity": velocidade_media, 
                    "altitude_max": altura_maxima,
                    "distancia_max": distancia_total,
                }
            )
        else:
            return jsonify({"status": "error", "message": result.stderr}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def start_server():
    app.run(host="0.0.0.0", port=5000)


def stop_server():
    os.kill(os.getpid(), signal.SIGINT)


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
