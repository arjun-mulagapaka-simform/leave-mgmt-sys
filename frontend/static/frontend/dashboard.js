document.addEventListener("DOMContentLoaded", async () => {
    try {
        // Welcome sign
        await welcome_sign();

        // Leave balance display
        await leave_balance_display();

        // adding pending leaves button
        await pending_leaves_button_display();

    } catch (e) {
        console.error("Dashboard error:", e);
    }
});

async function pending_leaves_button_display() {
    const userStr = localStorage.getItem("currentUser");

    if (!userStr) return;

    const user = JSON.parse(userStr); // <- parse it

    if (user.role !== roles["employee"]) {
        document.querySelector(".actions").innerHTML += `
            <a href="${BASE_URL + "leaves/pending"}" class="btn btn-warning">
                Pending Approvals
            </a>
        `;
    }
}

async function fetch_leave_balance() {
    const accessToken = localStorage.getItem("accessToken");
    try {
        const response = await authFetch(BASE_URL + "leaves/balance/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            }
        })
        const data = await response.json();
        return data["leave balance"];
    } catch (e) {
        console.error("Dashboard error:", e);
    }
}

async function welcome_sign() {
    const response = await getCurrentUser();
    const user = response.user;
    localStorage.setItem("currentUser", JSON.stringify(user));
    document.querySelector("h2").innerText = `Welcome, ${user.first_name + " " + user.last_name} 👋`;
}

async function leave_balance_display() {
    const balance = await fetch_leave_balance();

    const balanceCardsContainer = document.querySelector(".cards");

    if (balance) {
        for (const [type, value] of Object.entries(balance)) {
            balanceCardsContainer.innerHTML += `
                <div class="card">
                    <h5>${leave_type[type]}</h5>
                    <p>${value} days</p>
                </div>
            `;
        }
    } else {
        balanceCardsContainer.innerHTML = `<p>No leave balance data found!</p>`;
    }
}
