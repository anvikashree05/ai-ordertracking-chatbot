async function sendMessage() {
    let input = document.getElementById("message");
    let message = input.value;
    
    if (message.trim() === "") {
        return;
    }

    const chatBox = document.getElementById("chat-box");

    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.textContent = "You: " + message;
    chatBox.appendChild(userMsg);

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    const typingMsg = document.createElement('div');
typingMsg.className = 'message bot';
typingMsg.textContent = "Tracking your request...";
chatBox.appendChild(typingMsg);

chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

await new Promise(resolve =>
    setTimeout(resolve, 1000)
);
        typingMsg.remove();

        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        botMsg.textContent = "Bot: " + data.response;
        chatBox.appendChild(botMsg);

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        console.error('Error:', error);
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
       botMsg.textContent =
       "Bot: Sorry, I couldn't process your request. Please try again.";
        chatBox.appendChild(botMsg);

        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

document.getElementById("message").addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
window.onload = function() {

    const chatBox =
        document.getElementById("chat-box");

    chatBox.scrollTop =
        chatBox.scrollHeight;

};
window.onload = function() {

    const chatBox =
        document.getElementById("chat-box");

    chatBox.scrollTop =
        chatBox.scrollHeight;

    document.getElementById("message").focus();
};