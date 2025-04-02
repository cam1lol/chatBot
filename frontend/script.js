// Obtener los elementos de la UI
const chatBox = document.querySelector('#chat-box');
const inputField = document.querySelector('#user-input');
const sendButton = document.querySelector('#send-btn');

// Función para enviar un mensaje
sendButton.addEventListener('click', async (event) => {
    event.preventDefault();  // Esto previene la recarga de la página

    const userMessage = inputField.value;
    if (!userMessage) return;

    // Mostrar el mensaje del usuario
    displayMessage(userMessage, 'user');

    // Enviar el mensaje al backend para obtener la respuesta del bot
    const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    });
    const data = await response.json();

    // Mostrar la respuesta del bot
    if (data.response) {
        displayMessage(data.response, 'bot');
    }
});

// Función para mostrar los mensajes en el chat
function displayMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerHTML = `
        <img src="${sender === 'user' ? 'avatar1.png' : 'avatar2.png'}" alt="Avatar" class="avatar">
        <p class="text">${message}</p>
    `;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;  // Desplazar hacia abajo automáticamente
}
