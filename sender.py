import requests
import json

def send_message(message):
    # Reemplaza estos valores con tu token de bot y el ID del chat
    bot_token = "8242825417:AAHS5y43tAG5KV3Btadx1Kvz7nRXvFkFyAg"
    chat_id = "6444484639"

    url1 = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = {
        'chat_id': chat_id,
        'text': message
    }

    response = requests.post(url1, data=data)

    print(response.status_code)
    print(response.json())