Chatbot con Flask, OpenAI y Wikipedia

Este es un chatbot basado en inteligencia artificial que utiliza la API de OpenAI para generar respuestas, además de buscar información en Wikipedia cuando es necesario. El backend está desarrollado en Python con Flask y se conecta a una base de datos SQLite para almacenar las conversaciones.

🚀 Características

Utiliza OpenAI GPT-3.5 para generar respuestas.

Consulta Wikipedia cuando el modelo no tiene una respuesta directa.

Base de datos SQLite para almacenar conversaciones.

Implementado con Flask como backend.

Integración con un frontend en JavaScript.

📂 Estructura del Proyecto

chatBot/
│── backend/                # Backend en Flask
│   │── app.py              # Archivo principal con API REST
│   │── chatbot.db          # Base de datos SQLite
│   │── dataset/            # Carpeta con el dataset en JSON
│   │── requirements.txt    # Dependencias del proyecto
│── frontend/               # Frontend en JavaScript (HTML, CSS, JS)
│── README.md               # Este archivo

🔧 Instalación y Configuración

1️⃣ Clonar el repositorio

git clone https://github.com/tu-usuario/chatBot.git
cd chatBot/backend

2️⃣ Crear un entorno virtual (opcional pero recomendado)

python -m venv venv
source venv/bin/activate   # En macOS/Linux
venv\Scripts\activate      # En Windows

3️⃣ Instalar dependencias

pip install -r requirements.txt

4️⃣ Configurar variables de entorno

Crea un archivo .env dentro de la carpeta backend/ y agrega tu clave de OpenAI:

OPENAI_API_KEY=tu_clave_api

5️⃣ Ejecutar el backend

python app.py

El servidor se ejecutará en: http://127.0.0.1:5000

6️⃣ Probar con Postman o Frontend

Puedes probar el chatbot enviando una petición POST a http://127.0.0.1:5000/chat con un JSON:

{
    "message": "Hola"
}


📌 Tecnologías Usadas

Flask (API REST)

OpenAI API (GPT-3.5)

Wikipedia API (búsqueda de información)

SQLite (almacenamiento de conversaciones)

JavaScript, HTML, CSS (Frontend)

🛠 Futuras Mejoras

Agregar autenticación de usuarios.

Mejorar la UI del frontend.

Implementar una base de datos más robusta.

Ampliar el dataset de entrenamiento.

👨‍💻 Autor

Desarrollado por Camilo Ayala.
📧 Contacto: kmilo0230@gmail.com
