import { createPaymentForm } from '../components/PaymentForm.js';
import { BookingServices } from '../services/BookingServices.js';
import { CartStorageServices } from '../services/CartStorageServices.js';
import { StripeServices } from '../services/StripeServices.js';

// Helper local para empaquetar los datos del localStorage
function getBookingLocal() {
    const roomsStorage = CartStorageServices.getRooms();
    const bookingStorage = CartStorageServices.getBooking();
    if (!roomsStorage.length || !bookingStorage) return null;

    return {
        check_in: bookingStorage.checkin,
        check_out: bookingStorage.checkout,
        total: bookingStorage.total,
        room_ids: roomsStorage.map(room => room.roomId)
    };
}

document.addEventListener("DOMContentLoaded", () => {

    // PASO 1: Cargar UI
    const ui = createPaymentForm();
    if (!ui) return console.error("No se pudo inicializar el formulario.");

    // PASO 2: Inicializar Stripe
    StripeServices.initialize("pk_test_51TPTwGQgce7IB1FgFvUXbkfE37AvTCQKDgj7kyS4FhvtBlMTF2Dsu3KJO4SjkN1noEIhOzkGsTPClFRElkcVU0mB00zaAC3kak", ui.cardElementId);

    // PASO 3: Mostrar total en botón
    const booking = getBookingLocal();
    if (booking && ui.submitBtn) {
        ui.submitBtn.textContent = `Pagar $${booking.total}`;
    }

    // PASO 4: Evento submit
    ui.form.addEventListener("submit", async (e) => {
        e.preventDefault();

        //authRequire();

        if (!booking) return alert("No hay información de reserva activa.");

        ui.submitBtn.textContent = "Procesando pago...";
        ui.submitBtn.disabled = true;

        try {
            // Generar token Stripe
            const stripeToken = await StripeServices.createToken();

            // Enviar a API / BookingServices
            const response = await BookingServices.createBooking(stripeToken, booking);

            if (response && response.ok) {
                alert("¡Pago y reserva procesados con éxito!");
                localStorage.removeItem("booking");
                localStorage.removeItem("rooms");
                ui.form.reset();
                StripeServices.clear();
                ui.submitBtn.textContent = "Pagado";
            } else {
                const errorData = await response.json();
                alert(errorData.detail || "Error en el servidor");
                ui.submitBtn.disabled = false;
                ui.submitBtn.textContent = `Pagar $${booking.total}`;
            }

        } catch (error) {
            console.error(error);
            alert(error.message || "Error de conexión o tarjeta rechazada.");
            ui.submitBtn.disabled = false;
            ui.submitBtn.textContent = `Pagar $${booking.total}`;
        }
    });
});