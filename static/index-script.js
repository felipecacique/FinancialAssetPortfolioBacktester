// Wait of the DOM to fully load
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded");
    // Get form, buttons, and error message elements
    const loginForm = document.getElementById("login-form");
    const loginButton = document.getElementById("login-button");
    const registerButton = document.getElementById("register-button");
    const errorMessage = document.getElementById("error-message");

    // Listen for form submission
    loginForm.addEventListener("submit", async (e) => {
        console.log("loginForm submit");
        e.preventDefault();

        // Get username and password for the form
        const username = e.target.username.value;
        const password = e.target.password.value;

        try {
            // Send POST request to the server with user data
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password }),

            });

            // Parse the response as JSON
            const data = await response.json();
            console.log(data);
            // Check if login was successful
            if (data.success) {
                console.log("Login successfull");
                // Display to dashboard after successful login
                window.location.href = "/dashboard";
            } else {
                // Display error message if login failed
                errorMessage.textContent = "Invalid username or password";
            }
        } catch (error) {
            // Log any errors that occur
            console.error("Error:", error);
        }
    });

    
    // Listen for registration button click
    registerButton.addEventListener("click", () => {
        console.log("registerButton click");
        const username = loginForm.username.value;
        const password = loginForm.password.value;

        if (!username || !password) {
            displayErrorMessage("Both username and password are required.");
        } else if (password.length < 6) {
            displayErrorMessage("Password must be at least 6 characters.");
        } else {
            registerUser(username, password);
        }
    });


    // Function to display an error message
    function displayErrorMessage(message) {
        errorMessage.textContent = message;
    }

    // Function to register a user
    async function registerUser(username, password) {
        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            console.log(data);
            if (data.success) {
                console.log("Registration successful!");
                displayErrorMessage("Registration successful!");
            } else {
                console.log("Registration failed");
                displayErrorMessage(data.message);
            }
        } catch (error) {
            console.error("Error:", error)
        }
    }
    
});
