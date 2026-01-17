# Importamos las librerías necesarias
from flask import Flask, render_template, request, jsonify
import os
from google.cloud import dialogflow  # Librería para conectar con Dialogflow
import uuid  # Para generar IDs únicos si es necesario

# ==================== CONFIGURACIÓN DE CREDENCIALES ====================
# Esto permite usar las credenciales de forma segura
# Localmente: usa el archivo credentials.json
# En Railway: usa una variable de entorno (te explico después)
if os.environ.get('GOOGLE_CREDENTIALS'):
    # Si hay una variable de entorno con el JSON completo, la guardamos en un archivo temporal
    with open('credentials.json', 'w') as f:
        f.write(os.environ.get('GOOGLE_CREDENTIALS'))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
else:
    # Localmente, usa el archivo que pusiste en la carpeta
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

# ==================== CONFIGURACIÓN DE FLASK ====================
app = Flask(__name__)

# REEMPLAZA ESTO CON TU PROJECT ID DE DIALOGFLOW (lo ves en la consola de Dialogflow)
PROJECT_ID = "tecmibot-mbgq"  # Ejemplo: "tecmina-chatbot-1234"

# ==================== FUNCIÓN PARA CONSULTAR DIALOGFLOW ====================
def detect_intent(project_id, session_id, text, language_code='es'):
    """
    Esta función envía el mensaje del usuario a Dialogflow y recibe la respuesta.
    - project_id: ID de tu proyecto en Google Cloud
    - session_id: ID único de la conversación (para mantener contexto)
    - text: Mensaje del usuario
    - language_code: 'es' para español
    """
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session_path, "query_input": query_input}
    )

    # Devuelve solo el texto de respuesta del bot
    return response.query_result.fulfillment_text

# ==================== RUTAS DE LA WEB ====================
@app.route('/')
def home():
    """Sirve la página principal"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Recibe mensaje del usuario (desde JavaScript) y responde con Dialogflow"""
    data = request.get_json()
    user_message = data['message']
    session_id = data['session_id']  # ID de sesión que viene del navegador

    # Obtenemos respuesta de Dialogflow
    bot_response = detect_intent(PROJECT_ID, session_id, user_message)

    return jsonify({'response': bot_response})

# ==================== INICIAR LA APP ====================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)