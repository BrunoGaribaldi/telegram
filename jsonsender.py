import requests



def enviar():
    # URL de FlytBase
       # URL de FlytBase
    url = "https://api.flytbase.com/v2/integrations/webhook/6900081026671ac289bfd766"

    # Headers con tu token de autorización
    headers = {
        "Authorization": "Bearer TOKEN AQUI",   # 👈 pegá tu token
        "Content-Type": "application/json"
    }

    # Tu JSON
    payload = {
        "timestamp": 1759445058883,
        "severity": 2,
        "description": "High temperature",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "altitude_msl": 100,
        "metadata": {
            "sensor_id": "TempSensor12A",
            "temperature": 50.2,
            "battery_level": 80
        }
    }
    # POST a FlytBase

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # <- esto hace tire excepción
    return response.json()   

    