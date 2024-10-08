window.addEventListener('load', (e) => {
    fetch('http://localhost:8000/chats', {
        method: 'GET',
        headers:{
            'Content-type': 'application/json',
            'Accept': 'application/json',
        },
    }).then(response => response.json())
    .then(resp => {
        const list = document.getElementById("chatThreads");
        for(let i = 0; i < resp.length; i++){
            node = document.createElement("li");
            node.setAttribute('data-session-id', resp[i][0]);
            node.innerHTML = resp[i][1];
            a = document.createElement("a");
            a.style.color = 'white';
            a.style.textDecoration = 'none';
            a.setAttribute("href", `?chatId=${resp[i][0]}`);
            a.appendChild(node);
            list.appendChild(a);
        }
        if(window.location.search.indexOf("chatId") > 0){
            const chatId = Number(new URLSearchParams(window.location.search).get("chatId"));
            document.querySelector(`[data-session-id="${chatId}"`).classList.add('active');
            window.chatId = chatId;
        }
    })
    if(window.location.search.indexOf("chatId") > 0){
        const chatId = new URLSearchParams(window.location.search).get("chatId");
        window.chatId = chatId;
        fetch(`http://localhost:8000/chat/${chatId}`, {
        method: 'GET',
        headers:{
            'Content-type': 'application/json',
            'Accept': 'application/json',
        },
        }).then(response => response.json())
        .then(resp => {
            for(let i = 0; i < resp.length; i++){
                appendUserMessage(resp[i][0]);
                appendAssistantMessage(resp[i][1]);
            }
        }) 
    }
});

function appendUserMessage(message){
    const chatWindow = document.querySelector('.chat-window');
    const userMessageHTML = `
      <div class="user-message">
        <div class="message">${message}</div>
      </div>
    `;
    chatWindow.insertAdjacentHTML('beforeend', userMessageHTML);
}

function appendAssistantMessage(message){
    const botMessageHTML = `
    <div class="bot-message">
    <div class="message">${message}</div>
    </div>
    `;
    document.querySelector('.chat-window').insertAdjacentHTML('beforeend', botMessageHTML);
}

function handleAJAXCall() {
    document.getElementById("loading").innerHTML = 'TaxGPT is typing...';
    document.getElementById("sendBtn").setAttribute('disabled', true);
    document.getElementById("cancelBtn").setAttribute('disabled', true);
    fetch('http://localhost:8000/', {
        method: 'POST',
        headers:{
            'Content-type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            prompt: document.getElementById('userInput').value,
            id: window.chatId || null,
        })
    })
    .then(response=> response.json())
    .then(resp => {
        appendAssistantMessage(resp?.ans[0]);
        window.chatId=resp?.session_id
    }).finally(() => {
        document.getElementById("loading").innerHTML = '';
        document.getElementById("sendBtn").removeAttribute('disabled');
        document.getElementById("cancelBtn").removeAttribute('disabled');
    });
}

document.getElementById('sendBtn').addEventListener('click', function() {
  const message = document.getElementById('userInput').value;
  if (message) {
    appendUserMessage(message);
    handleAJAXCall();
    document.getElementById('userInput').value = '';
  }
});

document.getElementById("cancelBtn").addEventListener('click', function(){
    document.getElementById('userInput').value = '';
});