const BASE_URL = "http://127.0.0.1:8000/";

document.addEventListener("DOMContentLoaded", () => {
    const refreshToken = localStorage.getItem("refreshToken");

    // If already logged in, skip login page
    if (refreshToken) {
        window.location.href = BASE_URL + "leaves/dashboard/";
    }
});

async function login(event) {
    event.preventDefault();

    const email = document.getElementById("id_email").value;
    const password = document.getElementById("id_password").value;

    try {
        const response = await fetch(BASE_URL + "user/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(event)
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || "Login failed");
            return;
        }

        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);

        window.location.href = BASE_URL;

    } catch (e) {
        showError("Something went wrong");
        console.error(e);
    }
}

function showError(message) {
    const container = document.getElementById("login-errors");
    if (container) {
        container.innerText = message;
    }
}

function getCSRFToken(event) {
    const form = event.target;
    return form.querySelector('[name=csrfmiddlewaretoken]').value;
}