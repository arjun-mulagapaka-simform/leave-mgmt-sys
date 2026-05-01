const BASE_URL = "http://127.0.0.1:8000/";

document.addEventListener("DOMContentLoaded", () => {
    const navlinks = document.getElementById("nav-links");

    if (!navlinks) return; // prevent null crash

    const refreshToken = localStorage.getItem("refreshToken");

    if (refreshToken) {
        navlinks.hidden = false;
    } else {
        navlinks.hidden = true;
    }
});

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