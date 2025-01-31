function sendMessage() {
    var userQuestion = document.getElementById("user_input").value;

    if (userQuestion.trim() === "") return;

    var chatbox = document.getElementById("chatbox");

    // Display the user's message
    chatbox.innerHTML += "<div class='user-message'><strong>You:</strong> " + userQuestion + "</div>";

    // Send the user's message to the server
    fetch('/get_faq', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user_question=' + encodeURIComponent(userQuestion),
    })
    .then(response => response.json())
    .then(data => {
        // Display the bot's response
        chatbox.innerHTML += "<div class='bot-message'><strong>Bot:</strong> " + data.answer + "</div>";

        // Hide recommendations after the first message is sent
        hideRecommendations();

        // Scroll to the bottom of the chatbox
        chatbox.scrollTop = chatbox.scrollHeight;

        // Clear the input field
        document.getElementById("user_input").value = "";
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayRecommendations(chatbox) {
    var recommendations = [
        "What is Artificial Intelligence?",
        "What is Machine Learning?",
        "What is Deep Learning?",
        "How does AI impact healthcare?"
    ];

    // Add a recommendation button for each question
    recommendations.forEach(function(question) {
        chatbox.innerHTML += "<div class='bot-message'><button class='recommendation-button' onclick='askRecommendedQuestion(\"" + question + "\")'>" + question + "</button></div>";
    });
}

function hideRecommendations() {
    var recommendations = document.querySelectorAll('.recommendation-button');
    recommendations.forEach(function(button) {
        button.style.display = 'none';
    });
}

function askRecommendedQuestion(question) {
    var chatbox = document.getElementById("chatbox");

    // Display the recommended question as if the user asked it
    chatbox.innerHTML += "<div class='user-message'><strong>You:</strong> " + question + "</div>";

    // Send the recommended question to the server
    fetch('/get_faq', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user_question=' + encodeURIComponent(question),
    })
    .then(response => response.json())
    .then(data => {
        // Display the bot's response
        chatbox.innerHTML += "<div class='bot-message'><strong>Bot:</strong> " + data.answer + "</div>";

        // Hide recommendations after a selection
        hideRecommendations();

        // Scroll to the bottom of the chatbox
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function startSpeechRecognition() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.start();

    recognition.onresult = function(event) {
        var userQuestion = event.results[0][0].transcript;
        document.getElementById("user_input").value = userQuestion;
        sendMessage();
    }
}

window.onload = function() {
    // Display recommendations when the page loads
    var chatbox = document.getElementById("chatbox");
    displayRecommendations(chatbox);
}
