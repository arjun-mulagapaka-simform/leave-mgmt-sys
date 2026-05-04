const BASE_URL = "http://127.0.0.1:8000/";

document.addEventListener("DOMContentLoaded", () => {
    const refreshToken = localStorage.getItem("refreshToken");
    const navlinks = document.getElementById("nav-links");

    // Redirect to login if not authenticated
    if (!refreshToken) {
        window.location.href = BASE_URL + "login/";
        return;
    }

    // Show navbar if logged in
    if (navlinks) {
        navlinks.hidden = false;
    }
});

async function logout(event) {
    event.preventDefault();

    try {
        const refreshToken = localStorage.getItem("refreshToken");

        const response = await fetch(BASE_URL + "user/api/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        // Even if API fails, clear tokens
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        window.location.href = BASE_URL + "login/";

    } catch (e) {
        console.error(e);

        // fallback cleanup
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        window.location.href = BASE_URL + "login/";
    }
}