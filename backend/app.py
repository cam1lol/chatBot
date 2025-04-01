import os
import sqlite3
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
def get_db():
    conn = sqlite3.connect('chatbot.db')
    return conn

# Obtener la clave de API desde .env
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No se recibió el mensaje del usuario"}), 400

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response.choices[0].message.content

        # Guardar la conversación en la base de datos
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)",
                       (user_message, bot_reply))
        conn.commit()
        conn.close()

        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
