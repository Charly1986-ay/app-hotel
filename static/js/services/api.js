// apiClient.js
export async function apiFetch(url, options = {}) {
    let response;
    try {
        response = await fetch(url, {
            ...options,
            credentials: "include", // Crucial para tus cookies
            headers: {
                ...(options.body ? { "Content-Type": "application/json" } : {}),
                ...(options.headers || {})
            }
        });
    } catch (error) {
        console.error("Network error:", error);
        alert("Error de conexión con el servidor.");
        return null;
    }

    if (response.status === 401) {
        window.location.href = "/auth/login"; // Expulsa si la cookie venció
        return null;
    }

    return response;
}