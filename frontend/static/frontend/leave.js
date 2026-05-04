document.addEventListener("DOMContentLoaded", async () => {
    try {
        // get leave details
        await display_leave();
    } catch (error) {
        console.error("Leave Page error: ", error);
    }
});

async function get_leave() {
    const id = window.location.pathname.split("/").filter(Boolean).pop();
    const accessToken = localStorage.getItem("accessToken");
    try {
        const response = await authFetch(BASE_URL + "leaves/leaves/" + id, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            }
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}

async function display_leave() {
    try {
        const leave_data = await get_leave();
        const leaveCardContainer = document.getElementById("leave-details");
        leaveCardContainer.innerHTML += `
            <h4 id="leave-type">${leave_type[leave_data.leave_type]} leave request</h4>

            <p><strong>Dates:</strong> 
                <span id="leave-dates">${leave_data.start_date} to ${leave_data.end_date}</span>
            </p>

            <p><strong>Status:</strong> 
                <span id="leave-status">${status_map[leave_data.status]}</span>
            </p>

            <p><strong>Reason:</strong></p>
            <p id="leave-reason">${leave_data.reason}</p>
        `;
        if (leave_data.status != "pen") {
            leaveCardContainer.innerHTML += `
                <div id="actioned-by-container">
                    <p><strong>Actioned by:</strong></p>
                    <p id="actioned-by">${leave_data.actioned_by.first_name} ${leave_data.actioned_by.last_name}</p>
                </div>
            `;
            if (leave_data.status == "rej") {
                leaveCardContainer.innerHTML += `
                    <div id="rejection-container">
                        <p><strong>Rejection Reason:</strong></p>
                        <p id="leave-rejection">${leave_data.rejection_reason}</p>
                    </div>
                `;
            }
        }
    } catch (error) {
        console.error(error);
    }
}