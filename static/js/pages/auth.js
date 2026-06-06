import { AuthServices } from "../services/AuthServices.js";

const loginForm = document.querySelector('.auth-form');

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(loginForm);

    const response = await AuthServices.login(formData);

    if (!response) return;

    const json = await response.json();

    if (!response.ok) {
        alert(json.detail || 'Error de autenticación');
        return;
    }
    
    // 1. Leemos si hay una ruta guardada por el carrito, si no hay nada, por defecto va a la home "/"
    const redirectUrl = localStorage.getItem('redirect_after_login') || "/";
    
    // 2. Limpiamos la clave para no dejar basura en el navegador
    localStorage.removeItem('redirect_after_login');

    // 3. Redirección dinámica y fluida
    window.location.href = redirectUrl;
});