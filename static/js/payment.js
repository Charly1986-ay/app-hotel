// ======================================
// INITIALIZE STRIPE ELEMENTS
// ======================================
const stripe = Stripe("pk_test_51TPTwGQgce7IB1FgFvUXbkfE37AvTCQKDgj7kyS4FhvtBlMTF2Dsu3KJO4SjkN1noEIhOzkGsTPClFRElkcVU0mB00zaAC3kak"); // Pon tu pk_test_ aquí
const elements = stripe.elements();

// Creamos el componente de tarjeta oficial (trae número, fecha y CVC todo junto)
const cardElement = elements.create('card', {
    style: {
        base: {
            fontSize: '16px',
            color: '#32325d',
            '::placeholder': { color: '#aab7c4' }
        },
    }
});

// Lo montamos en el div de nuestro HTML
document.addEventListener('DOMContentLoaded', () => {
    cardElement.mount('#card-element');

    const paymentForm = document.querySelector('#paymentForm');

    if (paymentForm) {
        paymentForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // 1. MISMALÓGICA: Frenamos el GET nativo

            let booking = getBooking(); // Tu misma función de LocalStorage
            if (!booking) {
                alert("No hay información de reserva activa.");
                return;
            }

            const submitBtn = paymentForm.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.disabled = true;

            try {
                // 2. MISMA LÓGICA: Le pedimos el token a Stripe de forma segura
                const stripeResult = await stripe.createToken(cardElement);

                if (stripeResult.error) {
                    alert(`Error: ${stripeResult.error.message}`);
                    if (submitBtn) submitBtn.disabled = false;
                    return;
                }

                // Aquí está el token generado por Stripe de forma oficial
                const stripeToken = stripeResult.token.id; 

                // 3. MISMA LÓGICA: Tu POST exacto a FastAPI sin tocar una sola línea
                const response = await fetch("/payment", {
                    method: "POST",
                    credentials: "include",  
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ 
                        token: stripeToken, 
                        booking: booking 
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error en servidor: ${errorData.detail}`);
                    if (submitBtn) submitBtn.disabled = false;
                    return;
                }

                const data = await response.json();
                alert("¡Pago y reserva procesados con éxito!");
                
                localStorage.removeItem('booking');
                localStorage.removeItem('rooms');
                paymentForm.reset();
                cardElement.clear();

            } catch (error) {
                console.error("Error:", error);
                alert("Error de conexión.");
            } finally {
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }
});

// ======================================
// HELPER FUNCTIONS (La que se había perdido)
// ======================================
const getBooking = () => {
    let roomsStorage = JSON.parse(localStorage.getItem('rooms')) || [];
    if (roomsStorage.length === 0) return false;

    const roomIds = roomsStorage.map(room => room.roomId);
    let bookingStorage = JSON.parse(localStorage.getItem('booking')) || null;
    if (!bookingStorage) return false;

    return {
        check_in: bookingStorage.checkin,
        check_out: bookingStorage.checkout,
        room_ids: roomIds 
    };
}