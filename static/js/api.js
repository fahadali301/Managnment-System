// API wrapper with JWT
async function fetchWithJWT(url, method, token) {
    const response = await fetch(url, {
        method: method,
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
}

(function () {
    function storageKey(resource) {
        return "ms_" + resource;
    }

    function nowIso() {
        return new Date().toISOString();
    }

    function readLocal(resource) {
        const raw = localStorage.getItem(storageKey(resource));
        return raw ? JSON.parse(raw) : [];
    }

    function writeLocal(resource, data) {
        localStorage.setItem(storageKey(resource), JSON.stringify(data));
    }

    async function request(url, options) {
        const response = await fetch(url, options);
        let data = null;
        try {
            data = await response.json();
        } catch (e) {
            data = null;
        }
        return { response, data };
    }

    async function listItems(resource, endpoint) {
        try {
            const { response, data } = await request(endpoint, { method: "GET" });
            if (response.ok) {
                if (Array.isArray(data)) {
                    return { source: "api", items: data };
                }
                if (data && typeof data === "object") {
                    return { source: "api", items: [data] };
                }
            }
            if (response.status === 404 || response.status === 405) {
                return { source: "local", items: readLocal(resource) };
            }
            throw new Error("Request failed");
        } catch (error) {
            return { source: "local", items: readLocal(resource) };
        }
    }

    async function createItem(resource, endpoint, payload) {
        try {
            const token = localStorage.getItem("access");
            const headers = { "Content-Type": "application/json" };
            if (token) {
                headers.Authorization = "Bearer " + token;
            }

            const { response, data } = await request(endpoint, {
                method: "POST",
                headers,
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                return { source: "api", item: data };
            }
            if (response.status !== 404 && response.status !== 405) {
                const msg = data && data.detail ? data.detail : "Save failed";
                throw new Error(msg);
            }
        } catch (error) {
            if (error.message !== "Save failed") {
                // Continue to local fallback for unavailable endpoints.
            }
        }

        const localItems = readLocal(resource);
        const item = {
            id: Date.now(),
            ...payload,
            updated_at: nowIso(),
        };
        localItems.unshift(item);
        writeLocal(resource, localItems);
        return { source: "local", item };
    }

    window.AppAPI = {
        listItems,
        createItem,
    };
})();
