import requests
import time
import jsonsender

# Reemplaza 'TU_BOT_TOKEN_AQUI' con el token de tu bot
BOT_TOKEN = '8242825417:AAHS5y43tAG5KV3Btadx1Kvz7nRXvFkFyAg'
URL_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# El 'offset' es un marcador para decirle a la API
# qué actualizaciones ya hemos procesado.
offset = 0

def get_updates(offset):
    """Obtiene los mensajes nuevos desde la API de Telegram."""
    try:
        url = f"{URL_BASE}getUpdates?timeout=30&offset={offset}"
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error para códigos HTTP 4xx/5xx
        return response.json()['result']
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return []

def main():
    """Bucle principal para leer los mensajes."""
    global offset
    print("Iniciando el lector de mensajes del bot...")

    while True:
        updates = get_updates(offset)
        if updates:
            print(f"\nSe encontraron {len(updates)} mensajes nuevos:")
            for update in updates:
                # Actualiza el offset para no procesar este mensaje de nuevo
                offset = update['update_id'] + 1
                
                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    text = message.get('text', 'Mensaje sin texto')
                    user_name = message['from'].get('first_name', 'Desconocido')
                    
                    print(f"  - Chat ID: {chat_id}")
                    print(f"    Usuario: {user_name}")
                    print(f"    Mensaje: {text}\n")

                    if (text == "mision1"):
                        print("Iniciando misión 1...")
                        jsonsender.enviar()
                        print("Misión 1 enviada.")
                
                elif 'callback_query' in update:
                    # Si el usuario presiona un botón en línea
                    callback_query = update['callback_query']
                    chat_id = callback_query['message']['chat']['id']
                    data = callback_query['data']
                    user_name = callback_query['from'].get('first_name', 'Desconocido')

                    print(f"  - Chat ID: {chat_id}")
                    print(f"    Usuario: {user_name}")
                    print(f"    Datos del botón presionado: {data}\n")
        
        # Espera un momento antes de volver a preguntar
        time.sleep(1)

if __name__ == "__main__":
    main()