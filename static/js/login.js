// login.js
async function login(event) {
    event.preventDefault(); // Evitar que el form haga refresh

    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include", // importante para enviar/recibir cookies
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(errorData.detail || "Error en login");
            return;
        }

        const data = await response.json();
        const role = data.role; // Por ejemplo: "supervisor", "client", etc.

        // Redireccionar según rol
        switch(role) {
            case "client":
                window.location.href = "/dashboard";
                break;
            case "receptionist":
                window.location.href = "/reception";
                break;
            case "supervisor":
                window.location.href = "/supervisor-area";
                break;
            case "manager":
                window.location.href = "/manager-area";
                break;
            default:
                window.location.href = "/"; // fallback
        }

    } catch (err) {
        console.error("Error en login:", err);
        alert("Ocurrió un error, intente nuevamente");
    }
}

// Asignar el form
document.querySelector("#login-form").addEventListener("submit", login);