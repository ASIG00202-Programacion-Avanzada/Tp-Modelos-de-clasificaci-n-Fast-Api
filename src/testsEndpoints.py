import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Cargar payloads desde archivo
with open("./fixtures/payloads.json", "r") as file:
    payloads = json.load(file)

# ----------------------------
# Health check
# ----------------------------
response = requests.get(f"{BASE_URL}/health")
print("\n=== Health Check ===")
print("Status Code:", response.status_code)
print("Response:", response.json())

# ----------------------------
# Predicción individual (tomamos el primer objeto del JSON)
# ----------------------------
first_payload = payloads[0]  # primer objeto del array de payloads

response = requests.post(f"{BASE_URL}/predict", json=first_payload)
print("\n=== Individual Prediction ===")
print("Payload:", json.dumps(first_payload, indent=4))
print("Status Code:", response.status_code)
print("Response:", response.json())

# ----------------------------
# Predicción batch (todos los objetos)
# ----------------------------
batch_payload = {"batch": payloads}
response = requests.post(f"{BASE_URL}/predict_batch", json=batch_payload)
print("\n=== Batch Prediction ===")
print("Payload:", json.dumps(batch_payload, indent=4))
print("Status Code:", response.status_code)
print("Response:", response.json())

# ----------------------------
# Exportar Excel
# ----------------------------
response = requests.get(f"{BASE_URL}/export_predictions")
print("\n=== Export Predictions ===")
print("Status Code:", response.status_code)
print("Content-Disposition:", response.headers.get("Content-Disposition"))
