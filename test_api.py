import requests
import json

url = "http://127.0.0.1:5000/cinematica/caida-libre"
headers = {"Content-Type": "application/json"}
data = {
    "altura_inicial": 100,
    "tiempo_total_simulacion": 5,
    "num_puntos": 100
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")