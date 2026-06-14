import { AuthServices } from "../services/AuthServices.js";
import { validateEmail } from "../validators/userValidator.js";
import { redirectByUserRole } from "../utils/routes.js"; // ◄ Imported

const loginForm = document.querySelector('.auth-form');

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(loginForm);
    const email = formData.get('email');

    if (!validateEmail(email)) {
        alert('Ingrese un email válido');
        return;
    }

    const response = await AuthServices.login(formData);
    if (!response) return;

    const json = await response.json();

    if (!response.ok) {
        alert(json.detail || 'Error de autenticación');
        return;
    }

    // ◄ Enrutamiento dinámico, limpio y con soporte para el localStorage del cliente
    redirectByUserRole(json.role); 
});