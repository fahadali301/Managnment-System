// Dashboard charts logic
(function () {
    const enrollmentCanvas = document.getElementById("enrollmentChart");
    const departmentCanvas = document.getElementById("departmentChart");

    if (!enrollmentCanvas || !departmentCanvas || typeof Chart === "undefined") {
        return;
    }

    const enrollmentCtx = enrollmentCanvas.getContext("2d");
    new Chart(enrollmentCtx, {
        type: "line",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
            datasets: [{
                label: "Enrollments",
                data: [9800, 10300, 10850, 11200, 11620, 12040, 12230, 12480],
                backgroundColor: "rgba(79, 70, 229, 0.15)",
                borderColor: "rgba(79, 70, 229, 1)",
                borderWidth: 2,
                tension: 0.35,
                fill: true,
                pointRadius: 0,
            }],
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false } },
                y: { beginAtZero: false },
            },
        },
    });

    const departmentCtx = departmentCanvas.getContext("2d");
    new Chart(departmentCtx, {
        type: "doughnut",
        data: {
            labels: ["Engineering", "Business", "Medical", "Science", "Arts"],
            datasets: [{
                data: [30, 24, 18, 16, 12],
                backgroundColor: ["#4f46e5", "#06b6d4", "#22c55e", "#f59e0b", "#ef4444"],
                borderWidth: 0,
            }],
        },
        options: {
            responsive: true,
            plugins: { legend: { position: "bottom" } },
            cutout: "70%",
        },
    });
})();
