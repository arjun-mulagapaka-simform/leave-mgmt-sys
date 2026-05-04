const BASE_URL = "http://127.0.0.1:8000/";

document.addEventListener("DOMContentLoaded", async () => {
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

    try {
        // Welcome sign
        await welcome_sign();

        // Leave balance display
        await leave_balance_display();

        // Leave requests display
        await leave_requests_display();

    } catch (e) {
        console.error("Dashboard error:", e);
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
            window.location.href = "/login/";
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

        window.location.href = BASE_URL + "login/";

    } catch (e) {
        console.error(e);

        // fallback cleanup
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        window.location.href = BASE_URL + "login/";
    }
}

async function fetch_leave_balance() {
    const accessToken = localStorage.getItem("accessToken");
    try {
        const response = await authFetch(BASE_URL + "leaves/balance/",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            }
        })
        const data = await response.json();
        return data["leave balance"];
    }catch (e) {
        console.error("Dashboard error:", e);
    }
}

async function fetch_leave_requests(){
    const accessToken = localStorage.getItem("accessToken");
    try {
        const response = await authFetch(BASE_URL + "leaves/leaves/",{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            }
        })
        const data = await response.json();
        return data;
    }catch (e) {
        console.error("Dashboard error:", e);
    }
}

async function welcome_sign(){
    const response = await getCurrentUser();
    const user = response.user;
    localStorage.setItem("currentUser", JSON.stringify(user));
    document.querySelector("h2").innerText = `Welcome, ${user.first_name + " " + user.last_name} 👋`;
}

async function leave_balance_display(){
    const balance = await fetch_leave_balance();

    const balanceCardsContainer = document.querySelector(".cards");

    if (balance) {
        for (const [type, value] of Object.entries(balance)) {
            balanceCardsContainer.innerHTML += `
                <div class="card">
                    <h5>${type}</h5>
                    <p>${value} days</p>
                </div>
            `;
        }
    }else{
        balanceCardsContainer.innerHTML = `<p>No leave balance data found!</p>`;
    }
}

async function leave_requests_display(){
    const leaves = await fetch_leave_requests();

    const leaveCardsContainer = document.getElementById("table-body");

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

    if (leaves.count > 0) {
        for (const leave of leaves.results) {
            leaveCardsContainer.innerHTML += `
                <tr>
                    <td>${leave.leave_type}</td>
                    <td>${leave.start_date} - ${leave.end_date}</td>
                    <td><span class="${status_class[leave.status]}">${status_map[leave.status]}</span></td>
                </tr>
            `;
        }
    }else{
        leaveCardsContainer.innerHTML = `<p>No leave requests found!</p>`;
    }
}