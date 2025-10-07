import json

import requests
from flask import Flask, request, Response

# --- 1. CONFIGURACIÓN ---
# Coloca aquí los datos de tu aplicación de Meta Business.
# Es una buena práctica usar variables de entorno para no exponer tus tokens en el código.
# Ejemplo: os.environ.get('VERIFY_TOKEN')

VERIFY_TOKEN = "764884099482757"  # Token que eliges en la configuración del webhook en Meta
ACCESS_TOKEN = "TU_ACCESS_TOKEN_PERMANENTE"  # Token de acceso permanente de tu App de WhatsApp
PHONE_NUMBER_ID = "TU_PHONE_NUMBER_ID"  # El ID de tu número de teléfono comercial
VERSION = "v18.0"  # Versión de la API de Graph de Meta

# URL base para enviar mensajes a través de la API de Meta
META_API_URL = f"https://graph.facebook.com/{VERSION}/messages"

# --- 2. MANEJO DE ESTADO DE CONVERSACIÓN ---
# Usamos un diccionario para guardar el estado de cada usuario.
# La clave es el número de teléfono del usuario (wa_id) y el valor es su estado actual.
user_states = {}


# --- 3. FUNCIONES DE LÓGICA DEL BOT ---

def funcion_saludo(wa_id, message_text):
    """
    Maneja el saludo inicial y el reconocimiento de intenciones simples.
    Decide a qué función llamar a continuación.
    """
    # Respuestas a preguntas simples
    respuestas_simple = {
        "direccion": "Nuestra dirección principal es la Calle Ficticia #123, Ciudad Ejemplo.",
        "costos": "Nuestros costos de envío varían según el destino y el peso. ¿Te gustaría que te ayudara a rastrear un paquete?",
        "horario": "Estamos disponibles de Lunes a Viernes de 8am a 6pm.",
    }

    # Detectar palabras clave para decidir la acción
    texto_minusculas = message_text.lower()

    for keyword, answer in respuestas_simple.items():
        if keyword in texto_minusculas:
            send_whatsapp_message(wa_id, answer)
            return  # Responde y termina, no cambia de estado

    # Palabras clave para cambiar de función/estado
    if any(palabra in texto_minusculas for palabra in ["rastrear", "paquete", "guía", "envío"]):
        user_states[wa_id] = "IDENTIFICAR_PAQUETE"
        funcion_identificar_paquete(wa_id, "inicio")  # Inicia el flujo de rastreo
    elif any(palabra in texto_minusculas for palabra in ["menú", "opciones", "ayuda", "consultas"]):
        user_states[wa_id] = "MENU_CONSULTAS"
        funcion_menu_consultas(wa_id)
    elif any(palabra in texto_minusculas for palabra in ["adiós", "gracias", "chao", "hasta luego"]):
        funcion_despedida(wa_id)
    else:
        # Saludo por defecto si no se reconoce la intención
        message = (
            "¡Hola! 👋 Soy el asistente virtual de TuEmpresa.\n\n"
            "¿En qué puedo ayudarte hoy? Puedes escribirme:\n"
            "• 'Rastrear paquete' para consultar un envío.\n"
            "• 'Menú' para ver otras opciones.\n"
            "• O pregúntame por nuestra 'dirección' o 'costos'."
        )
        send_whatsapp_message(wa_id, message)
        user_states[wa_id] = "SALUDO"  # Establecemos un estado inicial


def funcion_identificar_paquete(wa_id, message_text):
    """
    Guía al usuario para que proporcione un número de guía y lo procesa.
    """
    if message_text == "inicio":
        send_whatsapp_message(wa_id, "Claro, por favor envíame el número de guía o de seguimiento de tu paquete.")
        return

    # Simulamos la validación del número de guía (ej. si tiene más de 5 caracteres)
    if len(message_text) > 5:
        # Llama a la función que buscaría el paquete (aquí simulada)
        info_paquete = buscar_paquete_en_base_de_datos(message_text)
        send_whatsapp_message(wa_id, info_paquete)

        # Después de dar la respuesta, vuelve al menú principal
        user_states[wa_id] = "SALUDO"
        send_whatsapp_message(wa_id, "¿Hay algo más en lo que pueda ayudarte?")
    else:
        send_whatsapp_message(wa_id,
                              "El número que enviaste parece muy corto. ¿Podrías verificarlo y enviármelo de nuevo?")


def funcion_menu_consultas(wa_id):
    """
    Despliega un menú interactivo con botones para que el usuario elija una opción.
    """
    # Estructura para un mensaje interactivo con botones
    interactive_message = {
        "type": "button",
        "body": {"text": "Selecciona una de las siguientes opciones:"},
        "action": {
            "buttons": [
                {"type": "reply", "reply": {"id": "btn_descripcion", "title": "Descripción de servicios"}},
                {"type": "reply", "reply": {"id": "btn_contacto", "title": "Contacto"}},
                {"type": "reply", "reply": {"id": "btn_pqr", "title": "PQR (Sugerencias)"}},
            ]
        }
    }
    send_whatsapp_message(wa_id, "", interactive_message)
    # El estado se mantiene en MENU_CONSULTAS hasta que el usuario presione un botón o escriba algo.


def funcion_despedida(wa_id):
    """
    Envía un mensaje de despedida y finaliza la sesión para ese usuario.
    """
    message = "¡Fue un gusto ayudarte! Que tengas un excelente día. 😊"
    send_whatsapp_message(wa_id, message)
    # Eliminamos al usuario del diccionario de estados para "olvidar" la conversación.
    if wa_id in user_states:
        del user_states[wa_id]


# --- 4. FUNCIONES DE APOYO ---

def send_whatsapp_message(to, text_message="", interactive_message=None):
    """
    Envía un mensaje de texto o interactivo a un usuario de WhatsApp a través de la API de Meta.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text" if text_message else "interactive",
    }

    if text_message:
        payload["text"] = {"body": text_message}
    elif interactive_message:
        payload["interactive"] = interactive_message

    try:
        response = requests.post(META_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Lanza un error si la petición falló
        print(f"Mensaje enviado a {to}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar mensaje a {to}: {e}")


def buscar_paquete_en_base_de_datos(tracking_number):
    """
    (SIMULACIÓN) Esta función simularía una consulta a una base de datos o API externa.
    En un caso real, aquí harías la llamada a tu sistema de gestión de envíos.
    """
    # Simulación: si la guía termina en "123", está en tránsito.
    if tracking_number.endswith("123"):
        return f"✅ Paquete con guía {tracking_number} encontrado.\n\nEstado: En tránsito.\nUbicación actual: Centro de distribución Bogotá.\nFecha estimada de entrega: Mañana."
    else:
        return f"❌ No encontramos un paquete con la guía {tracking_number}. Por favor, verifica el número e intenta de nuevo."


# --- 5. SERVIDOR WEB CON FLASK ---

app = Flask(__name__)


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Meta envía una petición GET para verificar que el webhook es válido.
    """
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args.get("hub.challenge"), 200
    return "Hello World", 200


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Recibe los mensajes entrantes de los usuarios.
    """
    data = request.get_json()
    print("Datos recibidos del webhook:", json.dumps(data, indent=2))

    # Verificar si es un mensaje de entrada
    if "entry" in data and "changes" in data["entry"][0]:
        change = data["entry"][0]["changes"][0]
        if "messages" in change["value"]:
            message_data = change["value"]["messages"][0]

            # Ignorar mensajes enviados por el propio negocio para evitar bucles
            if message_data.get("from") is None:
                return "OK", 200

            wa_id = message_data["from"]  # Número de WhatsApp del usuario

            # Determinar el tipo de mensaje (texto o respuesta a botón)
            if "text" in message_data:
                message_text = message_data["text"]["body"]
            elif "interactive" in message_data:
                # Es una respuesta a un botón interactivo
                button_reply_id = message_data["interactive"]["button_reply"]["id"]
                # Mapeamos el ID del botón a una acción
                if button_reply_id == "btn_descripcion":
                    message_text = "descripción de servicios"
                elif button_reply_id == "btn_contacto":
                    message_text = "contacto"
                elif button_reply_id == "btn_pqr":
                    message_text = "pqr"
                else:
                    message_text = "opción no reconocida"
            else:
                return "OK", 200  # No es un tipo de mensaje que manejamos

            # --- LÓGICA PRINCIPAL DE CONVERSACIÓN ---
            current_state = user_states.get(wa_id, "SALUDO")

            if current_state == "SALUDO":
                funcion_saludo(wa_id, message_text)
            elif current_state == "IDENTIFICAR_PAQUETE":
                funcion_identificar_paquete(wa_id, message_text)
            elif current_state == "MENU_CONSULTAS":
                # Procesar la respuesta del menú
                if "descripción" in message_text.lower():
                    send_whatsapp_message(wa_id,
                                          "Ofrecemos servicios de paquetería nacional, mensajería urgente y logística inversa.")
                elif "contacto" in message_text.lower():
                    send_whatsapp_message(wa_id,
                                          "Puedes contactarnos al teléfono 123456789 o escribiéndonos a este chat.")
                elif "pqr" in message_text.lower():
                    send_whatsapp_message(wa_id,
                                          "Para tu PQR, por favor envíanos un correo a soporte@tuempresa.com con el detalle de tu caso.")
                else:
                    send_whatsapp_message(wa_id, "No entendí esa opción. Por favor, elige una del menú.")

                # Después de responder, volvemos al estado de saludo
                user_states[wa_id] = "SALUDO"
                send_whatsapp_message(wa_id, "¿Necesitas algo más?")

    return "OK", 200


if __name__ == '__main__':
    # Para desarrollo, Flask se ejecuta en el puerto 5000.
    # Para producción, se recomienda usar un servidor WSGI como Gunicorn.
    app.run(port=5000, debug=True)