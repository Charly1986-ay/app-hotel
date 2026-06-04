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

        CartStorageServices.saveRoom(roomId, roomName, price);
    });
};