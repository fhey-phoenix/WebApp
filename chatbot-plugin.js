document.addEventListener("DOMContentLoaded", function() {
    
    const body = document.body;  
  
    // Create ChatBot container  
    const chatbotContainer = document.createElement('div');  
    chatbotContainer.id = 'chatbot-container';  
    chatbotContainer.innerHTML = `  
        <div id="chat-icon" class="chatbot-icon"></div>  
        <div id="chat-content" class="chatbot-content">  
            <div id="chat-header">  
                <span class="chat-title">Bot</span>  
                <span class="chat-status">Online</span>  
                <span id="close-icon" class="close-icon">&times;</span>  
            </div>  
            <div id="chat-container">  
                <div id="chat-output"></div>  
            </div>  
            <div id="chat-input-area">  
                <input type="text" id="user-input" placeholder="Send a message...">  
                <button id="send-btn">&#x27A4;</button>  
            </div>  
        </div>  
    `;  
    body.appendChild(chatbotContainer);  
  
    // ChatBot icon click event  
    const chatIcon = document.getElementById('chat-icon');  
    const chatContent = document.getElementById('chat-content');  
    const closeIcon = document.getElementById('close-icon');  
    const userInput = document.getElementById('user-input');  
    const sendBtn = document.getElementById('send-btn');  
    const chatOutput = document.getElementById('chat-output');
      
    // Add event listener to toggle the chat on icon click  
    chatIcon.addEventListener('click', function() {  
        chatbotContainer.classList.add('open');  
    });  
  
    // Add event listener to close the chat on close icon click  
    closeIcon.addEventListener('click', function() {  
        chatbotContainer.classList.remove('open');  
    });

    var lastBotMessageContainer = null;  
    // Add event listener to send button        
    sendBtn.addEventListener('click', function() {        
        // Get user input        
        var userquestion = userInput.value;
        userInput.value = '';
        displayUserMessage(userquestion);      
        // Create a new XMLHttpRequest      
        var xhr = new XMLHttpRequest();      
        xhr.open('POST', 'http://localhost:3000/generate-answer', true);      
        xhr.setRequestHeader('Content-Type', 'application/json');      
        // Send the request      
        xhr.send(JSON.stringify({ userquestion }));      
        console.log(userquestion);    
    
        var lastBotMessageContainer = null;  
    
        // Handle the response      
        xhr.onreadystatechange = function () {    
            console.log("state", xhr.readyState);    
    
            if (xhr.readyState === 3) {      
                var responseText = xhr.responseText;  
                console.log(responseText);    
                try {    
                    displayBotMessage(responseText, false);  
                } catch(e) {  
                    console.error(e);   
                    console.log("error");     
                }      
            } else if (xhr.readyState === 4) {  
                var responseText = xhr.responseText;  
                console.log(responseText);    
                try {    
                    displayBotMessage(responseText, true);  
                } catch(e) {  
                    console.error(e);   
                    console.log("error");     
                }    
            }  
        };      
    });    
    
    function displayUserMessage(userquestion) {    
        // Check if message is not empty        
        if (userquestion.trim() !== '') {        
            // Get current time      
            var timestamp = new Date().toLocaleTimeString();      
    
            // Add user message to chat    
            chatOutput.innerHTML += `    
            <div class="message-info user-info">      
                <img src="profile.png"" class="message-icon">      
                <span>You</span>      
                <span class="message-timestamp">${timestamp}</span>      
            </div>    
            <div class="message-container user">    
                <div class="message-box">${userquestion}</div>      
            </div>    
            `;      
        }  
    }  
    
    function displayBotMessage(botanswer, isFinal = false) {      
        // Check if message is not empty          
        if (botanswer.trim() !== '') {          
            // Get current time        
            var timestamp = new Date().toLocaleTimeString();    
      
            if(!lastBotMessageContainer && !isFinal) {    
      
                // Create a new container for the bot icon and timestamp  
                var botInfoContainer = document.createElement('div');  
                botInfoContainer.classList.add('message-info', 'bot-info');  
                botInfoContainer.innerHTML = `  
                    <img src="chatbot.png" class="message-icon">  
                    <span>Bot</span>        
                    <span class="message-timestamp">${timestamp}</span>`;  
      
                // Append the new container to the chat output  
                chatOutput.appendChild(botInfoContainer);  
      
                lastBotMessageContainer = document.createElement('div');    
                lastBotMessageContainer.classList.add('message-container', 'bot');    
                chatOutput.appendChild(lastBotMessageContainer);
            }    
      
            var messageBox = lastBotMessageContainer.querySelector('.message-box');    
            if(!messageBox) {    
                messageBox = document.createElement('div');    
                messageBox.classList.add('message-box');    
                lastBotMessageContainer.appendChild(messageBox);    
            }    
            messageBox.innerText = botanswer;    
      
            if(isFinal) {    
                lastBotMessageContainer = null;    
            }
            // Use requestAnimationFrame to ensure the DOM has been painted before scrolling  
            requestAnimationFrame(() => {  
                chatOutput.scrollTop = chatOutput.scrollHeight;  
            });    
        }            
    }  
    
    // Add event listener to user input to trigger send button on enter key  
    userInput.addEventListener('keypress', function(e) {  
        if (e.key === 'Enter') {  
            sendBtn.click();
            userInput.value = '';
        }  
    });  

});  
