const BASE_URL = "http://127.0.0.1:8000/";

document.addEventListener("DOMContentLoaded", () => {
    const refreshToken = localStorage.getItem("refreshToken");
    const navlinks = document.getElementById("nav-links");

    if (!navlinks) return; // prevent null crash

    if (!refreshToken) {
        window.location.href = BASE_URL + "login/";
        navlinks.hidden = true;
    }else{
        navlinks.hidden = false;
    }
});

async function login(event) {
    event.preventDefault();

    const email = document.getElementById("id_email").value;
    const password = document.getElementById("id_password").value;

    try {
        console.log(BASE_URL);
        const response = await fetch(BASE_URL + "api/token/", {
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

async function logout(event) {
    event.preventDefault();
    console.log("logout triggered");
    try {
        const refreshToken = localStorage.getItem("refreshToken");
        const response = await fetch(BASE_URL + "api/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "refresh": refreshToken })
        });

        if (response.status == 200) {
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            window.location.href = BASE_URL + "login/";
        } else {
            alert(response.status);
        }

    } catch (e) {
        console.log(e);
    }
}

