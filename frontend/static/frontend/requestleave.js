document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("leave-request-form");

    form.addEventListener("submit", submit_request);
});

async function submit_request(e){
    e.preventDefault();
    const leaveType = document.getElementById("leave_type").value;
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;
    const reason = document.getElementById("reason").value;

    const payload = {
        leave_type: leaveType,
        start_date: startDate,
        end_date: endDate,
        reason: reason
    };

    try {
        const res = await authFetch(BASE_URL + "leaves/leaves/", {
            method: "POST",
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            document.getElementById("leave-errors").innerText = data;
            return;
        }

        // Success
        alert("Leave request submitted successfully!");
        window.location.href = BASE_URL;

    } catch (err) {
        console.error(err);
        document.getElementById("leave-errors").innerText = "An unexpected error occurred.";
    }
}