let nick = prompt("Enter your nickname");

let input = document.getElementById("input");

input.focus(); // Set keyboard focus

// Register for notification of new messages using EventSource 
let chat = new EventSource("/chat");

chat.addEventListener("chat", event => {
    // When a chat message arrives

    let div = document.createElement("div"); // Create a <div>

    div.append(event.data); // Add text from the message

    input.before(div); // And add div before input

    input.scrollIntoView(); // Ensure input elt is visible 
});

// Post the user's messages to the server using fetch 
input.addEventListener("change", () => {  // When the user strikes return

    fetch("/chat", { // Start an HTTP request to this url.

        method: "POST", // Make it a POST request with body

        body: nick + ": " + input.value // set to the user's nick and input.

    })

        .catch(e => console.error); // Ignore response, but log any errors.

    input.value = ""; // Clear the input 
});
