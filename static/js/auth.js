window.addEventListener('load', (event) => {
    let email = document.querySelector('#email');
    let password = document.querySelector('#password');

    const form = document.querySelector('.auth-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const data = new FormData(form);

        try {
            const response = await fetch('auth/login', {
                method: 'POST',
                body: data
            });

            const json = response.json();
            console.log(json);
        } catch (error) {
            console.error("Error al obtener el JSON:", error);
        }
    });
});