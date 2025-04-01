import json
import random

# Nombre del archivo JSON
DATASET_FILE = "chat_dataset.json"

# Base de datos de preguntas y respuestas
dataset = [
    {"input": "Hola", "output": "¡Hola! ¿Cómo estás?"},
    {"input": "¿Cómo te llamas?", "output": "Soy un chatbot, ¿y tú?"},
    {"input": "Cuéntame un chiste", "output": "¿Qué le dice un jardinero a otro? ¡Disfrutemos mientras podamos!"},
    {"input": "Estoy triste", "output": "Lo siento. ¿Quieres contarme qué te pasa?"},
    {"input": "Gracias", "output": "¡De nada! 😊"},
    {"input": "Adiós", "output": "¡Hasta pronto! Fue un gusto hablar contigo."}
]

# Guardar dataset en JSON
def save_dataset():
    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    print(f"✅ Dataset guardado en {DATASET_FILE}")

# Ejecutar solo si se ejecuta este archivo directamente
if __name__ == "__main__":
    save_dataset()
