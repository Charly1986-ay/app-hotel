window.addEventListener('load', () => {

    const form = document.querySelector('.auth-form');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const data = new FormData(form);

        try {

            const response = await fetch('/auth/login', {
                method: 'POST',
                body: data,
                credentials: 'include'
            });

            const json = await response.json();

            console.log(json);

            if (!response.ok) {
                alert(json.detail || 'Error de autenticación');
                return;
            }

            // redirect ejemplo
            window.location.href = "/";

        } catch (error) {
            console.error("Error:", error);
        }
    });
});