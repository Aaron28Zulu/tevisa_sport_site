// static/js/chatbot.js

document.addEventListener("DOMContentLoaded", function () {
    const chatbotOpen = document.getElementById('chatbot-open');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbot = document.getElementById('chatbot');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotInput = document.getElementById('chatbot-user-input');
    const chatbotMessages = document.getElementById('chatbot-messages');

    // Open chatbot
    chatbotOpen.addEventListener('click', () => {
        chatbot.style.display = 'block';
        chatbotOpen.style.display = 'none';
    });

    // Close chatbot
    chatbotClose.addEventListener('click', () => {
        chatbot.style.display = 'none';
        chatbotOpen.style.display = 'block';
    });

    // Send message
    chatbotSend.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (message === "") return;

        appendMessage('You', message);
        chatbotInput.value = '';

        // Send message to backend
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
            .then(response => response.json())
            .then(data => {
                if (data.reply) {
                    appendMessage('Chatbot', data.reply);
                } else {
                    appendMessage('Chatbot', "I'm sorry, I didn't understand that.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                appendMessage('Chatbot', 'An error occurred. Please try again later.');
            });
    }

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chatbot-message');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
});
