import { UserServices } from "../services/UserServices.js"

const registerForm = document.querySelector('.auth-form');

registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    console.log("SUBMIT JS EJECUTADO");

    const formData = new FormData(registerForm);

    const response = await UserServices.register(formData);

    if (!response) return;

    const json = await response.json();

    if (!response.ok) {
        alert(json.detail || 'Error al registrar un usuario');
        return;
    }

    const redirectUrl = localStorage.getItem('redirect_after_login') || "/";    
  
    localStorage.removeItem('redirect_after_login');

    window.location.href = redirectUrl;
});