document.addEventListener("DOMContentLoaded", function () {
    const fileUploadForm = document.getElementById("fileUploadForm");
    const link = document.getElementById("linkInput");
    const apiKey = document.getElementById('keyInput');
    const chatMessages = document.getElementById("chatMessages");
    const messageInput = document.getElementById("messageInput");
    const sendMessageButton = document.getElementById("sendMessage");
    const userInputpdf = document.getElementById("pdf_text");
    const loadingSpinner = document.getElementById("loadingSpinner"); // Add this element

    fileUploadForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append("link", link.value);
        formData.append("key", apiKey.value); // Append the API key
        console.log(link.value)
        console.log(apiKey.value)

        // Show loading spinner while uploading
        loadingSpinner.style.display = "block";

        // Send the PDF file to the server
        fetch("http://localhost:8000/upload_data/", { // Update the URL as needed
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                // Hide loading spinner after upload
                loadingSpinner.style.display = "none";

                // Display the response from the server in the chat
                chatMessages.innerHTML += `<div><strong>User:</strong>got-it !</div>`;
            })
            .catch((error) => {
                // Hide loading spinner on error
                loadingSpinner.style.display = "none";

                console.error("Error uploading PDF:", error);
            });
    });


    sendMessageButton.addEventListener("click", function() {
        var userMessage = messageInput.value;
        if (userMessage.trim() !== "") {
            displayMessage("You", userMessage);

            // Get the send URL from the data attribute
            // const sendUrl = sendButton.getAttribute("data-send-url");

            messageInput.value = "";
            // You can add AJAX code here to send the user message to the server
                // Send user message to server using AJAX
                sendUserMessageToServer(userMessage);
            }
        });



        messageInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Prevent the default Enter key behavior (e.g., new line)
                sendMessageButton.click();
            }
        });



        function displayMessage(sender, message) {
            const messageDiv = document.createElement("div");
            // messageDiv.style.paddingTop = '20px'

            console.log(sender);
            if(sender == 'You'){
                messageDiv.className = "message_you";
                messageDiv.style.backgroundColor = "#69B4AD";

            }
            else if(sender == 'bot'){
                messageDiv.className = "message_bot";
                messageDiv.style.borderBottom = "1px solid black";
                messageDiv.style.marginBottom = "20px";


            }
            else{
            messageDiv.className = "else_section";
            }
            messageDiv.style.fontSize = "20px";
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatMessages.appendChild(messageDiv);

            // chatLog.scrollTop = chatLog.scrollHeight;
        }


        function sendUserMessageToServer(message) {
            console.log(message);
            fetch("http://localhost:8000/chat_with_bot/", { // Update the URL as needed
            method: "POST",
            body: JSON.stringify({ message }),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                // Display the response from the server in the chat
                console.log(data);
                displayMessage('bot' , data.output);
            })
            .catch((error) => {
                console.error("Error sending message:", error);
            });

        }


        userInputpdf.addEventListener('keydown', function (event) {
            var pdfmessage = userInputpdf.value;
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault(); // Prevent the default Enter key behavior (e.g., new line)
                // sendButtonpdf.click();
                sendpdfToServer(pdfmessage);

                // Clear the textarea after sending the message
                userInputpdf.value = '';
            }
        });

        console.log(pdf_text);
    function sendpdfToServer(pdf_text) {
        console.log(pdf_text);
        fetch("http://localhost:8000/d/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                "pdf_text": pdf_text


            })
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
    // Function to get CSRF token from cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
    }
});






