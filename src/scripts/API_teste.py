import time
import requests
from datetime import datetime, timedelta
import random

"""API não tem nada a haver com o servidor/programa, é apenas um teste para enviar dados para o servidor"""

url = "http://localhost:5000/gps"  # Endpoint do seu backend

# Parâmetros iniciais para simulação
latitude = -23.55052
longitude = -46.633308
data_base = datetime.now()

for i in range(10):  # Envia 10 pontos de teste
    data = (data_base + timedelta(minutes=i)).strftime("%d/%m/%Y")
    hora = (data_base + timedelta(minutes=i)).strftime("%H:%M:%S")
    latitude += random.uniform(0.00005, 0.00015)
    longitude += random.uniform(-0.00015, -0.00005)
    ponto = {
        "data": data,
        "hora": hora,
        "latitude": round(latitude, 5),
        "longitude": round(longitude, 6),
    }
    print(f"Enviando: {ponto}")
    response = requests.post(url, json=ponto)
    print(f"Resposta: {response.status_code} - {response.text}")
    time.sleep(2)
