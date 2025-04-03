// Obtener los elementos de la UI
const chatBox = document.querySelector('#chat-box');
const inputField = document.querySelector('#user-input');
const sendButton = document.querySelector('#send-btn');

console.log("Script cargado correctamente");

// Función para enviar un mensaje
async function sendMessage() {
    console.log("sendMessage() ejecutado");

    const userMessage = inputField.value.trim();
    console.log("Mensaje del usuario:", userMessage);
    
    if (!userMessage) return;

    displayMessage(userMessage, 'user');
    inputField.value = '';
    inputField.focus();

    sendButton.disabled = true;

    try {
        console.log("Enviando mensaje al backend...");
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage }),
        });

        console.log("Respuesta recibida:", response);
        
        if (!response.ok) throw new Error('Error en el servidor');

        const data = await response.json();
        console.log("Datos del servidor:", data);

        displayMessage(data.response, 'bot');
    } catch (error) {
        console.error("Error en la solicitud:", error);
        displayMessage('Lo siento, hubo un error. Inténtalo de nuevo.', 'bot');
    } finally {
        sendButton.disabled = false; 
    }
}

// Eventos para enviar mensaje con botón y con "Enter"
sendButton.addEventListener('click', (event) => {
    console.log("Botón de enviar presionado");
    event.preventDefault(); 
    sendMessage();
});

inputField.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        console.log("Enter presionado");
        event.preventDefault();
        sendMessage();
    }
});

// Función para mostrar los mensajes en el chat
function displayMessage(message, sender) {
    console.log(`Mostrando mensaje de ${sender}:`, message);

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    const avatarPath = `assets/${sender === 'user' ? 'avatar2.jpeg' : 'avatar1.jpeg'}`;
    messageDiv.innerHTML = `
        <img src="${avatarPath}" alt="Avatar" class="avatar">
        <p class="text">${message}</p>
    `;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
