import sqlite3
import openai
from flask import Flask, request, jsonify
import json
import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

app = Flask(__name__)

# Configuración de la base de datos
def get_db():
    conn = sqlite3.connect('chatbot.db')
    return conn

# Establecer la clave de API de OpenAI
openai.api_key = ''

# Cargar el dataset de ejemplos desde el archivo JSON
def cargar_dataset():
    with open(os.path.join('dataset', 'chat_dataset.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

dataset = cargar_dataset()  # Cargar los datos al iniciar la aplicación

# Lista de intenciones y patrones
intenciones = {
    'saludo': ['hola', 'buenos días', 'qué tal', 'cómo estás', 'hola, ¿cómo estás?'],
    'despedida': ['adiós', 'hasta luego', 'nos vemos', 'chau'],
    'clima': ['qué tiempo hace', 'cómo está el clima', 'qué clima hay hoy'],
    'consulta': ['cómo estás', 'quién eres', 'qué haces']
}

def identificar_intencion(mensaje):
    """Identifica la intención del mensaje"""
    mensaje = mensaje.lower()
    for intencion, patrones in intenciones.items():
        for patron in patrones:
            if re.search(patron, mensaje):
                return intencion
    return None

def obtener_respuesta_dataset(mensaje):
    """Busca una respuesta en el dataset cargado"""
    for item in dataset:
        if mensaje.lower() in item['input'].lower():
            return item['output']
    return None

# Entrenar el modelo de clasificación
def train_model():
    """Entrenar el modelo para identificar las intenciones del usuario"""
    inputs = [entry["input"] for entry in dataset]
    outputs = [entry["output"] for entry in dataset]
    
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(inputs)
    
    model = MultinomialNB()
    model.fit(X, outputs)
    
    return model, vectorizer

# Entrenar el modelo al iniciar la aplicación
model, vectorizer = train_model()

@app.route('/chat', methods=['POST'])
def chat():
    # Obtén el mensaje del usuario
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No se recibió el mensaje del usuario"}), 400

    # Primero intenta encontrar una respuesta en el dataset
    bot_reply = obtener_respuesta_dataset(user_message)

    if bot_reply:  # Si hay respuesta en el dataset
        pass
    else:  # Si no hay respuesta en el dataset, usa el modelo entrenado
        intencion = model.predict(vectorizer.transform([user_message]))[0]
        
        if intencion == 'saludo':
            bot_reply = "¡Hola! ¿Cómo te ha ido hoy?"
        elif intencion == 'despedida':
            bot_reply = "¡Adiós! ¡Nos vemos pronto!"
        elif intencion == 'clima':
            bot_reply = "Lo siento, no tengo acceso al clima actual, pero puedes consultar una aplicación de clima."
        elif intencion == 'consulta':
            bot_reply = "Soy un chatbot, ¿en qué puedo ayudarte?"
        else:
            # Si no se detecta ninguna intención, el chatbot hace una consulta a OpenAI
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response['choices'][0]['message']['content'].strip()

    # Guardar la conversación en la base de datos
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)",
                   (user_message, bot_reply))
    conn.commit()
    conn.close()

    # Retornar la respuesta en formato JSON
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
