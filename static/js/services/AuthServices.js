// js/services/AuthServices.js

export const AuthServices = {
    /**
     * Envía las credenciales directamente en formato multipart/form-data.     
     * @param {FormData} formData - El objeto capturado directamente del HTML.
     */
    login: async (formData) => {
        // Hacemos el fetch directamente apuntando al endpoint de FastAPI
        const response = await fetch('/auth/login', {
            method: 'POST',            
            credentials: 'include',            
            body: formData
        });

        return response;
    },
    
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
            
            if (!response.ok) {
                return null;
            }
           
            const json = await response.json();
            return json;

        } catch (error) {
            console.error("Error de red en la verificación:", error);
            return null; 
        }
    }
};