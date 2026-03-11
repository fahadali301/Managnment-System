// API wrapper with JWT
async function fetchWithJWT(url, method, token) {
    const response = await fetch(url, {
        method: method,
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
}