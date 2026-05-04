document.addEventListener("DOMContentLoaded", async () => {
    try {
        // Leave requests display
        await pending_requests_display();

    } catch (e) {
        console.error("Error:", e);
    }
});

async function fetch_pending_requests() {
    try {
        const response = await authFetch(BASE_URL + "leaves/pending/", {
            method: "GET"
        })
        const data = await response.json();
        return data;
    } catch (e) {
        console.error("Error:", e);
    }
}

async function pending_requests_display() {
    const leaves = await fetch_pending_requests();
    const container = document.getElementById("table-body");

    container.innerHTML = "";

    if (leaves.count > 0) {
        for (const leave of leaves.results) {
            container.innerHTML += `
                <tr>
                    <td>${leave_type[leave.leave_type]}</td>
                    <td>${leave.start_date} → ${leave.end_date}</td>
                    <td>
                        <span class="${status_class[leave.status]}">
                            ${status_map[leave.status]}
                        </span>
                    </td>
                    <td>${leave.reason}</td>
                    <td>
                        <button class="btn btn-success btn-sm"
                            onclick="approveLeave(${leave.id})">
                            Approve
                        </button>

                        <button class="btn btn-danger btn-sm"
                            onclick="showRejectBox(${leave.id})">
                            Reject
                        </button>

                        <div id="reject-box-${leave.id}" style="display:none; margin-top:8px;">
                            <textarea id="reject-reason-${leave.id}" 
                                class="form-control" 
                                maxlength="500"
                                placeholder="Enter rejection reason..."></textarea>

                            <button class="btn btn-danger btn-sm mt-1"
                                onclick="rejectLeave(${leave.id})">
                                Submit
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }
    } else {
        container.innerHTML = `
            <tr>
                <td colspan="5" class="text-center">
                    No pending requests!
                </td>
            </tr>
        `;
    }
}

function showRejectBox(id) {
    const box = document.getElementById(`reject-box-${id}`);
    box.style.display = box.style.display === "none" ? "block" : "none";
}

async function approveLeave(id) {
    const res = await authFetch(`${BASE_URL}leaves/${id}/approve/`, {
        method: "PATCH",
        body: JSON.stringify({
            "status": "apr"
        })
    });

    if (res.ok) {
        alert("Approved");
        pending_requests_display(); // refresh
    } else {
        alert("Failed");
        console.log(res.error);
    }
}

async function rejectLeave(id) {
    const reason = document.getElementById(`reject-reason-${id}`).value;

    if (!reason) {
        alert("Rejection reason required");
        return;
    }

    const res = await authFetch(`${BASE_URL}leaves/${id}/reject/`, {
        method: "PATCH",
        body: JSON.stringify({
            "status": "rej",
            "rejection_reason": reason
        })
    });

    if (res.ok) {
        alert("Acknowledged!");
        pending_requests_display(); // refresh
    } else {
        alert("Failed");
        console.log(res);
    }
}