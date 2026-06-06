// js/utils/session.js

import { AuthServices } from "../services/AuthServices.js";

export const authRequire = async () => {
    const jsonResponse = await AuthServices.checkAuth();

    if (!jsonResponse) {
        window.location.href = '/auth/login';
        return false; // ◄ Cambiado: Avisamos que falló
    }

    const role = jsonResponse.role;

    switch (role) {
        case 'client':
            console.log('Cliente autenticado');
            return true; // ◄ Cambiado: Avisamos que todo OK

        case 'receptionist':
            console.log('Redirigido al modulo Recepcionista');
            // window.location.href = '/recepcion';
            return true;

        case 'supervisor':
            console.log('Redirigido al modulo Supervisor');
            // window.location.href = '/supervisor/dashboard';
            return true;

        case 'manager':
            console.log('Redirigido al modulo Manager');
            // window.location.href = '/admin/dashboard';
            return true;

        default:
            console.log('Error, rol inexistente');
            window.location.href = '/auth/login';
            return false; // ◄ Cambiado
    }
}