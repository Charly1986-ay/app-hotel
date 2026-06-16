export const UserServices = {
    /**
     * Recibe el FormData directo del control del formulario HTML y lo procesa.
     * @param {FormData} formData 
     */
    register: async (formData) => {
        console.log("SCRIPT CARGADO - REGISTRO");

        // Transforma el FormData que vino del control de la página a formato de texto plano
        const encodedData = new URLSearchParams(formData);

        const response = await fetch('/api/register', { 
            method: 'POST',            
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: encodedData // Mandamos la data compatible
        });

        return response;
    },

    /**
     * Recibe el FormData directo del control del formulario de edición.
     * @param {FormData} formData 
     */
    update: async (formData) => {
        // Transforma el FormData que vino del control de la página a formato de texto plano
        const encodedData = new URLSearchParams(formData);

        const response = await fetch('/api/update', {
            method: 'POST',            
            credentials: 'include', // Para que viaje la cookie de sesión y FastAPI sepa quién sos
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: encodedData
        });

        return response;
    }
}