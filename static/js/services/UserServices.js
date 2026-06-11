export const UserServices = {
    /**
     * Envía las credenciales directamente en formato multipart/form-data.     
     * @param {FormData} formData - El objeto capturado directamente del HTML.
     */

    register: async (formData) => {
        console.log("SCRIPT CARGADO");
        const response = await fetch('/api/register', {
            method: 'POST',            
            credentials: 'include',            
            body: formData
        });

        return response;
    },

    update: async (formData) => {
        const response = await fetch('/api/update', {
            method: 'POST',            
            credentials: 'include',            
            body: formData
        });

        return response;
    }
}