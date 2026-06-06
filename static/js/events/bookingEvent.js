import { CartStorageServices } from "../services/CartStorageServices.js";

export const initBookingEvents = () => {
    document.addEventListener('click', (event) => {
        const btn = event.target.closest('.btn-booking');
        if (!btn) return;

        const article = btn.closest('article');
        if (!article) return;

        const roomId = article.dataset.roomId;
        const roomName = article.dataset.roomName;
        const price = article.dataset.price;

        // 🌟 Capturamos la respuesta del carrito (true o false)
        const guardadoExitoso = CartStorageServices.saveRoom(roomId, roomName, price);

        // 🔒 Si devuelve true, desactivamos el botón por completo
        if (guardadoExitoso) {
            btn.disabled = true;
            btn.textContent = "Seleccionado";
            btn.style.pointerEvents = 'none'; // Refuerzo para anular por completo los clics del mouse
        }
    });
};