// ==================== CONFIGURACIÓN INICIAL ====================
// Generamos o recuperamos un ID único para la sesión (mantiene el contexto de la conversación)
function getSessionId() {
    let sessionId = localStorage.getItem('chatSessionId');
    if (!sessionId) {
        sessionId = crypto.randomUUID();  // ID único moderno
        localStorage.setItem('chatSessionId', sessionId);
    }
    return sessionId;
}

const sessionId = getSessionId();
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// ==================== FUNCIÓN PARA AGREGAR MENSAJES AL CHAT ====================
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    
    // Scroll automático al final
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ==================== MENSAJE DE BIENVENIDA DEL BOT ====================
addMessage('¡Hola! Soy el asistente virtual del Tecnologico nacional de Mexico/ instituto tecnologico de Minatitlán. ¿que documentos necesitas obtener? 😊');

// ==================== FUNCIÓN PARA ENVIAR MENSAJE ====================
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Mostrar mensaje del usuario
    addMessage(text, true);
    userInput.value = '';

    // Enviar al backend Flask
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId })
    });

    const data = await response.json();
    addMessage(data.response);  // Mostrar respuesta del bot
}

// ==================== EVENTOS ====================
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});