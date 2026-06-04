// js/services/AuthServices.js

export const AuthServices = {
    /**
     * Envía las credenciales directamente en formato multipart/form-data.
     * Compatible con: email: Annotated[str, Form()] y password: Annotated[str, Form()]
     * @param {FormData} formData - El objeto capturado directamente del HTML.
     */
    login: async (formData) => {
        // Hacemos el fetch directamente apuntando al endpoint de FastAPI
        const response = await fetch('/auth/login', {
            method: 'POST',
            // OBLIGATORIO: Permite que FastAPI te devuelva la cookie 'access_token' 
            // y que el navegador la guarde de forma segura.
            credentials: 'include',
            // NOTA: No declaramos Headers. Al pasar el formData, el navegador
            // escribe automáticamente el Content-Type correcto.
            body: formData
        });

        return response;
    },

    /**
     * Cierra la sesión en el backend
     */
    logout: async () => {
        try {
            const response = await fetch('/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });
            return response.ok;
        } catch (error) {
            console.error("Error en logout:", error);
            return false;
        }
    },


    checkAuth: async () => {
        try {
            const response = await fetch('/auth/me', {
                method: 'GET',
                credentials: 'include' // Obligatorio para cookies HttpOnly
            });

            // Si el backend responde con 401 o 403, 'response.ok' será false
            if (!response.ok) {
                return null;
            }

            // Si fue un 200 OK, convertimos y devolvemos el JSON con id y role
            const json = await response.json();
            return json;

        } catch (error) {
            console.error("Error de red en la verificación:", error);
            return null; // Ante una caída de red devolvemos null por seguridad
        }
    }
};