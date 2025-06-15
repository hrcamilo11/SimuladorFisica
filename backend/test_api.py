import requests
import json

url = 'http://localhost:5000/cinematica/caida-libre'
headers = {'Content-Type': 'application/json'}
data = {'altura_inicial': 10, 'tiempo_total_simulacion': 2}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
except requests.exceptions.ConnectionError as e:
    print(f"Error de conexión: {e}")
except Exception as e:
    print(f"Ocurrió un error: {e}")