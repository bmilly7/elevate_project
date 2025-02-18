let nameInput = document.getElementById("name-input");
let submitButton = document.getElementById("submit-btn");
let greetingOutput = document.getElementById("greeting-output");

async function fetchGreeting() {
    let name = nameInput.value.trim();

    

    try {
        // Send a request to the Django backend
        let response = await fetch(`/greet/?name=${encodeURIComponent(name)}`);

        // Check if the response is OK
        if (!response.ok) {
            throw new Error("Failed to fetch greeting.");
        }


    // Convert response to JSON
        let data = await response.json();

        greetingOutput.textContent = data.greeting || "No greeting received.";
    } catch (error) {
        console.error("Error fetching greeting:", error);
        greetingOutput.textContent = "An error occurred. Please try again.";
    }
}

// Add event listener to the button
submitButton.addEventListener("click", fetchGreeting);