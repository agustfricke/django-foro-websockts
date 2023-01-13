// Navbar Resposive
let button = document.querySelector('[data-mobile-menu]');
let mobileMenu = document.getElementById('mobile-menu');

button.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden')
});

// Alert
let alertButton = document.querySelector('[close]');
let alerta = document.getElementById('alerta');

if (alertButton) {
alertButton.addEventListener('click', () => {
    alerta.classList.toggle('hidden')
})
}


// WebSocket stuff 

const roomId = JSON.parse(document.getElementById('json-roomid').textContent)
const userName = JSON.parse(document.getElementById('json-username').textContent)

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/' + roomId + '/'
)

chatSocket.onmessage = function (e) {
    console.log('onmessage')
}

chatSocket.onclose = function (e) {
    console.log('onclose')
}

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.username == userName) {
        document.querySelector('#chat-body').innerHTML += 

        `<li class="flex justify-end">
        <div class="relative max-w-xl px-4 py-2 font-mono bg-claro rounded shadow">
            <span class="block">${data.message}</span>
        </div>
    </li>`
} else {
document.querySelector('#chat-body').innerHTML += 
    `<li class="flex justify-start">
        <div class="relative max-w-xl px-4 py-2 font-mono bg-rosa rounded shadow">
        <span class="block">${data.username} : ${data.message}</span>
        </div>
    </li>`
    }

}

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'room': roomId
    }))

    messageInputDom.value = '';
    return false
}



