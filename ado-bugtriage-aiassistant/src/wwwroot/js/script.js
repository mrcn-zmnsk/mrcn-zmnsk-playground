const messageList = document.getElementById('message-list');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

function buildWaitDiv() {
    const waitDiv = document.createElement('div');
    waitDiv.id = 'loading';
    waitDiv.classList.add('message', 'bot', 'dots');
    for (i = 0; i < 3; i++) {
        const d = document.createElement('span');
        d.textContent = '.';
        waitDiv.appendChild(d);
    }
    return waitDiv;
}

const waitDiv = buildWaitDiv();

function init() {
    messageList.appendChild(waitDiv);
    messageInput.focus();
    
    fetch('https://localhost:7228/AdoTriage')
        .then(response => response.json())
        .then(data => {
            messageList.removeChild(waitDiv);
            data.forEach(data => {                
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message', 'bot');
                messageDiv.innerHTML = marked.parse(data.text); 
                messageList.appendChild(messageDiv);
            });
        });
}



function sendMessage() {
    const messageText = messageInput.value;
    messageInput.value = '';

    if (messageText.trim() !== '') {

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'user');
        messageDiv.textContent = messageText;

        messageList.appendChild(messageDiv);
        messageList.appendChild(waitDiv);

        fetch('https://localhost:7228/AdoTriage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: messageText, author: 'user' })
        })
            .then(response => response.json())
            .then(data => {
                const responseDiv = document.createElement('div');
                responseDiv.classList.add('message', 'bot');
                responseDiv.innerHTML = marked.parse(data.text);

                messageList.removeChild(waitDiv);
                messageList.appendChild(responseDiv);

                
                messageInput.focus();
            });
    }
}

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

init();