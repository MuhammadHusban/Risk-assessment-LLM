// Add event listener for the Enter key on the message input
document.addEventListener("DOMContentLoaded", function() {
    const messageInput = document.getElementById("message");
    messageInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default action (form submission)
            sendMessage(); // Trigger the sendMessage function
        }
    });
});

function startChat() {
    const customerIdInput = document.getElementById("customerId");
    customerId = customerIdInput.value.trim();

    if (customerId === "") {
        alert("Please enter a valid Customer ID.");
        return;
    }

    // Hide Customer ID input section and show loading indicator
    document.getElementById("customerIdSection").style.display = "none";
    document.getElementById("loadingSection").style.display = "block";

    // Fetch data and display the risk assessment
    fetch('/start-chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Customer_ID: customerId }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.response) {
            document.getElementById("loadingSection").style.display = "none";
            document.getElementById("chatSection").style.display = "block";
            const chatOutput = document.getElementById("chatOutput");
            chatOutput.innerHTML += `<p class='bot'><strong>Risk Assessment:</strong> ${data.response}</p>`;
        } else {
            throw new Error("No response data received.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        // Hide loading section and show an error message
        document.getElementById("loadingSection").style.display = "none";
        alert("An error occurred while processing your request. Please try again.");
        document.getElementById("customerIdSection").style.display = "block";
    });
}

function sendMessage() {
    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim();

    if (message === "") return;  // Do nothing if the input is empty

    // Display the user's message in the chat window
    const chatOutput = document.getElementById("chatOutput");
    chatOutput.innerHTML += `<p class='user'>${message}</p>`;
    chatOutput.scrollTop = chatOutput.scrollHeight;

    // Clear the input field
    messageInput.value = "";

    // Show a loading indicator while waiting for the bot's response
    const loadingIndicator = document.createElement("p");
    loadingIndicator.className = "bot";
    loadingIndicator.textContent = "The bot is typing...";
    chatOutput.appendChild(loadingIndicator);
    chatOutput.scrollTop = chatOutput.scrollHeight;

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Customer_ID: customerId, query: message }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Remove the loading indicator
        chatOutput.removeChild(loadingIndicator);

        // Display the bot's response in the chat window
        chatOutput.innerHTML += `<p class='bot'>${data.response}</p>`;
        chatOutput.scrollTop = chatOutput.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);

        // Remove the loading indicator
        chatOutput.removeChild(loadingIndicator);

        // Display an error message in the chat window
        chatOutput.innerHTML += `<p class='bot'>An error occurred while processing your request. Please try again.</p>`;
        chatOutput.scrollTop = chatOutput.scrollHeight;
    });
}
