from flask import Flask, request, jsonify
import datetime
import json


app = Flask(__name__)


@app.route('/gps', methods=['POST'])
def receber_dados():
    dados = request.json

    with open("dadosRecebidos.json", "a", encoding = "utf-8") as f:
        json.dump(dados, f)
        f.write("\n")  # quebra de linha entre registros
    
    
    hora_atual = datetime.datetime.now() - datetime.timedelta(hours=3)
    hora_recebimento = hora_atual.strftime("%H:%M:%S")

    print(f"[{hora_recebimento}] Dados recebidos: {dados}")
    return jsonify({"status": "ok", "mensagem": "Dados recebidos com sucesso!"})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "mensagem": "pong"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)