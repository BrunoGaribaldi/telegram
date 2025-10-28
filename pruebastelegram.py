import requests
import time
import json
from datetime import datetime, timedelta, timezone
import jsonsender

# ================== Config ==================
BOT_TOKEN = "8242825417:AAHS5y43tAG5KV3Btadx1Kvz7nRXvFkFyAg"
URL_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}/"

POLL_TIMEOUT = 30          # long polling
SLEEP_BETWEEN_POLLS = 2    # para no ciclar fuerte
SESSION_TTL_SECS = 180     # ⏳ duración de la ventana (ajustá a gusto)

# Duración fija de la misión (10 min 13 s)
MISSION_DURATION = 12 * 60
#MISSION_DURATION = 20
mission_running = False
mission_start_time = 0
current_mission_name = None

# ================== Estado en memoria ==================
# sessions[chat_id] = {"started_at": datetime, "expires_at": datetime, "user_name": str}
sessions = {}
offset = 0  # Para no procesar mensajes viejos

# ================== Helpers de API ==================
def get_updates(offset):
    try:
        url = f"{URL_BASE}getUpdates?timeout={POLL_TIMEOUT}&offset={offset}"
        r = requests.get(url, timeout=POLL_TIMEOUT + 5)
        r.raise_for_status()
        return r.json().get("result", [])
    except requests.RequestException as e:
        print(f"[get_updates] Error: {e}")
        return []

def send_message(chat_id, text, reply_markup=None):
    url = f"{URL_BASE}sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if reply_markup is not None:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        r = requests.post(url, data=data, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"[send_message] Error: {e}")

def remove_keyboard(chat_id, text="Ventana cerrada. Escribí 'hola' para empezar de nuevo."):
    send_message(chat_id, text, reply_markup={"remove_keyboard": True})

# ================== Sesiones ==================

def now():
    return datetime.now(timezone.utc)

def is_session_active(chat_id):
    s = sessions.get(chat_id)
    if not s:
        return False
    if now() >= s["expires_at"]:
        sessions.pop(chat_id, None)
        return False
    return True

def touch_session(chat_id):
    if chat_id in sessions:
        sessions[chat_id]["expires_at"] = now() + timedelta(seconds=SESSION_TTL_SECS)

def start_session(chat_id, user_name):
    sessions[chat_id] = {
        "started_at": now(),
        "expires_at": now() + timedelta(seconds=SESSION_TTL_SECS),
        "user_name": user_name,
    }

def end_session(chat_id):
    sessions.pop(chat_id, None)

# ================== UI: Menú ==================
def main_menu_keyboard():
    return {
        "keyboard": [
            [{"text": "mision1"}],
            [{"text": "Lista de misiones"}],
            [{"text": "Cerrar"}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "is_persistent": True
    }

def send_main_menu(chat_id):
    send_message(
        chat_id,
        "Menú principal:\n•mision1\n• Lista de misiones\n• Cerrar",
        reply_markup=main_menu_keyboard()
    )

# ================== Lógica de comandos ==================
def handle_start_or_hola(chat_id, user_name):
    if is_session_active(chat_id):
        touch_session(chat_id)
        send_message(chat_id, f"Ya tenés una ventana activa, {user_name}. Usá el menú o escribí 'cerrar' para reiniciar.")
        return
    start_session(chat_id, user_name)
    send_message(chat_id, f"Hola, {user_name} 👋 Soy el bot de NQNPetrol. Inicié una ventana de {SESSION_TTL_SECS} segundos.")
    send_main_menu(chat_id)

def handle_lista_misiones(chat_id):
    if not is_session_active(chat_id):
        remove_keyboard(chat_id, "Tu ventana estaba cerrada por inactividad. Escribí 'hola' para abrir una nueva.")
        return
    touch_session(chat_id)
    send_message(chat_id, "Misiones disponibles:\n1. Perímetro Planta\n\nEscribí o tocá 'mision1'.")

def handle_mision1(chat_id):
    global mission_running, mission_start_time, current_mission_name

    if not is_session_active(chat_id):
        remove_keyboard(chat_id, "Tu ventana estaba cerrada por inactividad. Escribí 'hola' para abrir una nueva.")
        return

    touch_session(chat_id)

    # --- Control de misión activa ---
    if mission_running:
        elapsed = time.time() - mission_start_time
        remaining = int(MISSION_DURATION - elapsed)

        if remaining > 0:
            minutes, seconds = divmod(remaining, 60)
            send_message(
                chat_id,
                f"🚫 *Error al enviar misión.*\n"
                f"Actualmente se está ejecutando la misión 'Perímetro Planta'*.\n"
                f"Debes esperar {minutes} min {seconds} s para poder enviar otra."
            )
            return
        else:
            mission_running = False
            current_mission_name = None

    # --- Envío de nueva misión ---
    send_message(chat_id, "Iniciando misión 🚀")
    try:
        # Envío real (descomentá cuando uses FlytBase)
        jsonsender.enviar()
        mission_running = True
        mission_start_time = time.time()
        current_mission_name = "mision1"

        send_message(chat_id, "✅ Misión *Perímetro Planta* enviada correctamente.\nNo se podrá mandar otra hasta que finalice (~10 min 13 s).")

    except requests.exceptions.RequestException as e:
        send_message(chat_id, f"⚠️ Error al enviar la misión: Porfavor contacte con soporte")
    except Exception as e:
        send_message(chat_id, f"❌ Ocurrió un error inesperado: : Porfavor contacte con soporte")

def handle_cerrar(chat_id):
    if is_session_active(chat_id):
        end_session(chat_id)
    remove_keyboard(chat_id)

def handle_fallback(chat_id):
    if is_session_active(chat_id):
        touch_session(chat_id)
        send_message(chat_id, "No entendí tu mensaje 🤔 Probá con el menú.")
        send_main_menu(chat_id)
    else:
        send_message(chat_id, "No hay ventana activa. Escribí 'hola' para empezar.")

# ================== Ignorar mensajes viejos ==================
def clear_pending_updates():
    """Descarta mensajes pendientes antes de iniciar el loop."""
    global offset
    try:
        url = f"{URL_BASE}getUpdates?timeout=1"
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        data = r.json().get("result", [])
        if data:
            offset = data[-1]["update_id"] + 1
            print(f"[Init] Ignorando {len(data)} mensajes pendientes anteriores al arranque.")
        else:
            print("[Init] No hay mensajes pendientes.")
    except Exception as e:
        print(f"[Init] Error al limpiar mensajes pendientes: {e}")

# ================== Loop principal ==================
def main():
    global offset
    print("Bot iniciado con ventanas de conversación y control de misión…")

    # --- 🔥 Ignorar mensajes antiguos antes de iniciar ---
    clear_pending_updates()

    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                message = update["message"]
                chat_id = message["chat"]["id"]
                text = (message.get("text") or "").strip()
                user_name = message["from"].get("first_name", "Desconocido")

                if not is_session_active(chat_id) and chat_id in sessions:
                    end_session(chat_id)
                    remove_keyboard(chat_id, "⏳ La ventana expiró por inactividad. Escribí 'hola' para empezar de nuevo.")

                lower = text.lower()
                if lower in ("/start", "hola"):
                    handle_start_or_hola(chat_id, user_name)
                elif lower == "lista de misiones":
                    handle_lista_misiones(chat_id)
                elif lower == "mision1":
                    handle_mision1(chat_id)
                elif lower in ("cerrar", "/cerrar"):
                    handle_cerrar(chat_id)
                else:
                    handle_fallback(chat_id)

        time.sleep(SLEEP_BETWEEN_POLLS)

if __name__ == "__main__":
    main()
