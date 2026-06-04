import { CartStorageServices } from "../services/CartStorageServices.js";
import { createCartItem } from "./CartItem.js";

const getModal = () => document.querySelector("#modalRooms");
const getCartItems = () => document.querySelector("#cartItems");
const getTotalEl = () => document.querySelector("#itemsTotal");

export const ModalCart = {

    open() {
        const modal = getModal();
        if (!modal) return;

        this.render();
        modal.style.display = "block";
    },

    close() {
        const modal = getModal();
        if (modal) modal.style.display = "none";
    },

    render() {
        const container = getCartItems();
        const totalEl = getTotalEl();

        if (!container) return;

        const rooms = CartStorageServices.getRooms();
        container.innerHTML = '';

        if (rooms.length === 0) {
            container.innerHTML = 'No hay habitaciones seleccionadas.';
            if (totalEl) totalEl.textContent = 'Total: 0 USD';
            return;
        }

        rooms.forEach((room, index) => {
            const item = createCartItem(
                room.roomType,
                room.price,
                index,
                (i) => {
                    CartStorageServices.deleteRoom(i);
                    this.render();
                }
            );

            container.appendChild(item);
        });

        if (totalEl) {
            totalEl.textContent = `Total: ${CartStorageServices.getTotal()} USD`;
        }
    }
};