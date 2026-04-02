// Core JavaScript
console.log('Main JS Loaded');

(function () {
    function setSync(sourceText, online) {
        const dot = document.getElementById("sync-indicator");
        const text = document.getElementById("sync-text");
        if (!dot || !text) {
            return;
        }
        dot.classList.toggle("status-online", online);
        dot.classList.toggle("status-offline", !online);
        text.textContent = sourceText;
    }

    function initSidebarToggle() {
        const shell = document.getElementById("portal-shell");
        const toggleBtn = document.getElementById("sidebar-toggle");
        const backdrop = document.getElementById("sidebar-backdrop");
        if (!shell || !toggleBtn || !backdrop) {
            return;
        }

        function closeSidebar() {
            shell.classList.remove("sidebar-open");
            backdrop.classList.remove("active");
        }

        toggleBtn.addEventListener("click", function () {
            const isOpen = shell.classList.toggle("sidebar-open");
            backdrop.classList.toggle("active", isOpen);
        });

        backdrop.addEventListener("click", closeSidebar);
        window.addEventListener("resize", function () {
            if (window.innerWidth > 992) {
                closeSidebar();
            }
        });
    }

    function toText(value) {
        return value === null || value === undefined || value === "" ? "-" : String(value);
    }

    function renderRows(tbody, items) {
        if (!items.length) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted py-4">No records found</td></tr>';
            return;
        }
        tbody.innerHTML = items
            .map((item, index) => {
                const primary = item.name || item.username || item.full_name || item.title || "Untitled";
                const details = item.description || item.email || item.address || item.details || "-";
                const updated = item.updated_at || item.created_at || "-";
                return (
                    "<tr>" +
                    "<td>" + toText(item.id || index + 1) + "</td>" +
                    "<td>" + toText(primary) + "</td>" +
                    "<td>" + toText(details) + "</td>" +
                    "<td>" + toText(updated) + "</td>" +
                    "</tr>"
                );
            })
            .join("");
    }

    async function initRealtimeList() {
        const container = document.getElementById("realtime-list");
        if (!container || !window.AppAPI) {
            return;
        }

        const resource = container.dataset.resource;
        const endpoint = container.dataset.endpoint;
        const tbody = document.getElementById("list-body");
        const status = document.getElementById("list-status");
        const refreshBtn = document.getElementById("btn-refresh");
        let loading = false;

        async function load() {
            if (loading) {
                return;
            }
            loading = true;
            if (refreshBtn) {
                refreshBtn.disabled = true;
                refreshBtn.textContent = "Refreshing...";
            }

            const result = await window.AppAPI.listItems(resource, endpoint);
            renderRows(tbody, result.items || []);
            const online = result.source === "api";
            setSync(online ? "Synced from API" : "Local mode", online);
            if (status) {
                status.textContent = "Last update: " + new Date().toLocaleTimeString();
            }

            if (refreshBtn) {
                refreshBtn.disabled = false;
                refreshBtn.textContent = "Refresh";
            }
            loading = false;
        }

        await load();
        setInterval(load, 5000);

        if (refreshBtn) {
            refreshBtn.addEventListener("click", load);
        }
    }

    async function initRealtimeForm() {
        const container = document.getElementById("realtime-form");
        if (!container || !window.AppAPI) {
            return;
        }

        const form = document.getElementById("entity-form");
        const message = document.getElementById("form-message");
        const resource = container.dataset.resource;
        const endpoint = container.dataset.endpoint;
        const redirect = container.dataset.redirect;

        form.addEventListener("submit", async function (event) {
            event.preventDefault();
            const payload = Object.fromEntries(new FormData(form).entries());

            try {
                const result = await window.AppAPI.createItem(resource, endpoint, payload);
                message.className = "alert alert-success";
                message.textContent = result.source === "api" ? "Saved to API." : "Saved locally (offline mode).";
                message.style.display = "block";
                setSync(result.source === "api" ? "Synced from API" : "Local mode", result.source === "api");
                setTimeout(function () {
                    window.location.href = redirect;
                }, 800);
            } catch (error) {
                message.className = "alert alert-danger";
                message.textContent = error.message || "Unable to save.";
                message.style.display = "block";
            }
        });
    }

    initSidebarToggle();
    initRealtimeList();
    initRealtimeForm();
})();
