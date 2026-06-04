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

    // Si todo salió bien (ej: 200 o 201), se redirige a la home
    window.location.href = "/";
});


export const authRequire = async () => {
    // 1. El servicio ahora devuelve el objeto JSON o null
    const jsonResponse = await AuthServices.checkAuth();

    // 2. Si es null (no logueado / error), redirigimos y FRENAMOS el script
    if (!jsonResponse) {
        window.location.href = '/auth/login';
        return; // 👈 CRUCIAL para que no intente leer el 'role' de abajo
    }

    // 3. Leemos la propiedad exacta que manda FastAPI ('role')
    const role = jsonResponse.role;

    // 4. Enrutamiento inteligente en el futuro
    switch (role) {
        case 'client':
            console.log('Cliente autenticado');
            break;

        case 'receptionist':
            console.log('Redirigido al modulo Recepcionista');
            // window.location.href = '/recepcion';
            break;

        case 'supervisor':
            console.log('Redirigido al modulo Supervisor');
            // window.location.href = '/supervisor/dashboard';
            break;

        case 'manager':
            console.log('Redirigido al modulo Manager');
            // window.location.href = '/admin/dashboard';
            break;

        default:
            console.log('Error, rol inexistente');
            window.location.href = '/auth/login';
            break;
    }
}