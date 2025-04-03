import sqlite3
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Configurar Flask y habilitar CORS
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://127.0.0.1:5500"}})

# Cargar clave API de OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("La clave API de OpenAI no está configurada en el archivo .env")

openai.api_key = OPENAI_API_KEY

# Conexión a la base de datos
def get_db():
    return sqlite3.connect('chatbot.db')

# Cargar dataset desde JSON
def cargar_dataset():
    with open(os.path.join('dataset', 'chat_dataset.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

dataset = cargar_dataset()

# Entrenar modelo Naive Bayes
def train_model():
    """Entrenar el modelo con inputs y outputs del dataset"""
    inputs = [entry["input"] for entry in dataset]
    outputs = [entry["output"] for entry in dataset]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(inputs)

    model = MultinomialNB()
    model.fit(X, outputs)

    return model, vectorizer

# Entrenar modelo al iniciar
model, vectorizer = train_model()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No se recibió el mensaje del usuario"}), 400

    # Intentar predecir una respuesta con el modelo
    predicted_response = model.predict(vectorizer.transform([user_message]))[0]

    # Si no hay predicción, usar OpenAI
    if not predicted_response:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        predicted_response = response['choices'][0]['message']['content'].strip()

    # Guardar en la base de datos
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)",
                   (user_message, predicted_response))
    conn.commit()
    conn.close()

    return jsonify({"response": predicted_response})

if __name__ == '__main__':
    import os
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
    app.run(debug=True, use_reloader=False)
