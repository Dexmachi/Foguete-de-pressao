from flask import Flask, request, jsonify
import datetime
import json


app = Flask(__name__)


@app.route('/dados', methods=['POST'])
def receber_dados():
    dados = request.json

    with open("Prototipagem/backend/dadosRecebidos.json", "a") as f:
        json.dump(dados, f)
        f.write("\n")  # quebra de linha entre registros
    hora_recebimento = datetime.datetime.now().strftime("%H:%M:%S")
    
    print(f"[{hora_recebimento}] Dados recebidos: {dados}")
    return jsonify({"status": "ok", "mensagem": "Dados recebidos com sucesso!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
