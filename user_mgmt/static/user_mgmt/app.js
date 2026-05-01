async function login(event) {
    event.preventDefault();

    const email = document.getElementById("id_email").value;
    const password = document.getElementById("id_password").value;

    try {
        console.log(BASE_URL);
        const response = await fetch("http://127.0.0.1:8000/api/token/", {
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

        localStorage.setItem("accessToken",data["access"]);
        localStorage.setItem("refreshToken",data["refresh"]);

        window.location.href = BASE_URL + "leaves/dashboard/";

    } catch (e) {
        showError(e);
    }
}

async function showError(message) {
    const container = document.getElementById("login-errors");
    container.innerText = message;
}

function getCSRFToken(event){
    const form = event.target;
    const csrf_token = form.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrf_token;
}