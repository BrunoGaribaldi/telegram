import requests
import time
import jsonsender   # tu módulo externo

# Token y URL base del bot
BOT_TOKEN = "8242825417:AAHS5y43tAG5KV3Btadx1Kvz7nRXvFkFyAg"
URL_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}/"

offset = 0  # Para no procesar mensajes viejos


def get_updates(offset):
    """Obtiene mensajes nuevos desde la API de Telegram."""
    try:
        url = f"{URL_BASE}getUpdates?timeout=30&offset={offset}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['result']
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return []


def send_message(chat_id, message):
    """Envía un mensaje a un chat específico."""
    url = f"{URL_BASE}sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar mensaje: {e}")


def main():
    """Loop principal del bot."""
    global offset
    print("Bot iniciado...")

    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update['update_id'] + 1  # Avanzar offset

                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    text = message.get('text', '')
                    user_name = message['from'].get('first_name', 'Desconocido')

                    print(f"\nMensaje de {user_name}: {text}")

                    # Respuestas y acciones
                    if text.lower() == "hola":
                        send_message(chat_id, f"Hola, {user_name} 👋 soy el bot de NQNPetrol. ¿En qué te puedo ayudar?")

                    elif text.lower() == "mision1":
                        send_message(chat_id, "Iniciando misión 1 🚀")
                        #jsonsender.enviar()   # llamada a tu lógica externa
                        send_message(chat_id, "Misión 1 enviada ✅")
                    elif text.lower() == "lista de misiones":
                        send_message(chat_id, "Misiones disponibles:\n1. mision1 - Rodial")
                        send_message(chat_id, "Ingrese ie. mision1")

                    else:
                        send_message(chat_id, "No entendí tu mensaje 🤔")

        time.sleep(1)


if __name__ == "__main__":
    main()
