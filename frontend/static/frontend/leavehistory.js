document.addEventListener("DOMContentLoaded", async () => {
    try {
        // Leave requests display
        await leave_requests_display();

    } catch (e) {
        console.error("Dashboard error:", e);
    }
});

async function fetch_leave_requests() {
    const accessToken = localStorage.getItem("accessToken");
    try {
        const response = await authFetch(BASE_URL + "leaves/leaves/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            }
        })
        const data = await response.json();
        return data;
    } catch (e) {
        console.error("Dashboard error:", e);
    }
}

async function leave_requests_display() {
    const leaves = await fetch_leave_requests();

    const leaveCardsContainer = document.getElementById("table-body");

    if (leaves.count > 0) {
        for (const leave of leaves.results) {
            leaveCardsContainer.innerHTML += `
                <tr>
                    <td>${leave_type[leave.leave_type]}</td>
                    <td>${leave.start_date} -> ${leave.end_date}</td>
                    <td><span class="${status_class[leave.status]}">${status_map[leave.status]}</span></td>
                    <td><a href="${BASE_URL}leaves/${leave.id}">View</a></td>
                    </tr>
            `;
        }
    } else {
        leaveCardsContainer.innerHTML = `<tr>
                <td colspan="4" class="text-center">
                    No leave requests found!
                </td>
            </tr>`;
    }
}