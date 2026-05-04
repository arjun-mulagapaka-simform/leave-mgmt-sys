const BASE_URL = "http://127.0.0.1:8000/";

document.addEventListener("DOMContentLoaded", async () => {
    const refreshToken = localStorage.getItem("refreshToken");
    const navlinks = document.getElementById("nav-links");

    // Redirect to login if not authenticated
    if (!refreshToken) {
        window.location.href = BASE_URL + "login";
        return;
    }

    // Show navbar if logged in
    if (navlinks) {
        navlinks.hidden = false;
    }
});

async function authFetch(url, options = {}) {
    let accessToken = localStorage.getItem("accessToken");

    let response = await fetch(url, {
        ...options,
        headers: {
            ...(options.headers || {}),
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json"
        }
    });

    // If access token expired
    if (response.status === 401) {
        const refreshed = await refreshAccessToken();

        if (!refreshed) {
            window.location.href = "login";
            return;
        }

        // retry original request with new token
        accessToken = localStorage.getItem("accessToken");

        response = await fetch(url, {
            ...options,
            headers: {
                ...(options.headers || {}),
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        });
    }

    return response;
}

async function refreshAccessToken() {
    const refreshToken = localStorage.getItem("refreshToken");

    if (!refreshToken) return false;

    const res = await fetch(BASE_URL + "user/api/token/refresh/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ refresh: refreshToken })
    });

    if (!res.ok) return false;

    const data = await res.json();
    localStorage.setItem("refreshToken", data.refresh);
    localStorage.setItem("accessToken", data.access);

    return true;
}

async function getCurrentUser() {
    const accessToken = localStorage.getItem("accessToken");

    const response = await authFetch(BASE_URL + "user/api/me", {
        headers: {
            "Authorization": `Bearer ${accessToken}`
        }
    });

    if (!response.ok) {
        throw new Error("Not authenticated");
    }

    return await response.json();
}

async function logout(event) {
    event.preventDefault();

    try {
        const refreshToken = localStorage.getItem("refreshToken");

        const response = await authFetch(BASE_URL + "user/api/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        // Even if API fails, clear tokens
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("currentUser");

        window.location.href = BASE_URL + "login";

    } catch (e) {
        console.error(e);

        // fallback cleanup
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        window.location.href = BASE_URL + "login";
    }
}

const status_map = {
    "pen": "Pending",
    "rej": "Rejected",
    "apr": "Approved"
};

const status_class = {
    "pen": "badge bg-warning",
    "rej": "badge bg-danger",
    "apr": "badge bg-success"
};

const leave_type = {
    "paid": "Paid",
    "unpaid": "Unpaid",
    "compensation": "Compensation",
    "incident": "Incident"
};

const roles = {
    "employee": 2,
    "reporting manager": 3,
    "manager": 4,
    "hr": 5,
}