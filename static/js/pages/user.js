import { UserServices } from "../services/UserServices.js"
import { 
    validateEmail, 
    validateText, 
    validatePassword 
} from "../validators/userValidator.js";

const registerForm = document.querySelector('.auth-form');

registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(registerForm);

    const fullname = formData.get('full_name');
    const email = formData.get('email');
    const password = formData.get('password');
    const repeatPassword = formData.get('confirm_password');

    if (!validateText(fullname)) {
        alert('Ingrese un nombre válido');
        return;
    }

    if (!validateEmail(email)) {
        alert('Ingrese un email válido');
        return;
    }

    if (!validatePassword(password) || password !== repeatPassword){
        alert('Verifique las contraseñas');
        return;
    }

    const response = await UserServices.register(formData);

    if (!response) return;

    const json = await response.json();

    if (!response.ok) {
        alert(json.detail || 'Error al registrar un usuario');
        return;
    }

    alert("¡Registro exitoso! Por favor, inicia sesión para completar tu reserva.");
    
    // En lugar de ir directo a pagar sin credenciales, la mandamos al login tradicional
    window.location.href = "/auth/login";
});